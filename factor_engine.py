"""
Factor Engine Module
因子评分、时间对齐、影响力分析
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json


class FactorEngine:
    """因子分析引擎"""
    
    def __init__(self, factor_config_path: str = "factor_config.json"):
        """
        初始化因子引擎
        
        Args:
            factor_config_path: 因子配置文件路径
        """
        with open(factor_config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def calculate_event_impact_score(self, event: Dict) -> float:
        """
        计算事件的影响力分数
        
        公式: event_strength = 新闻重要性 × 主题相关度 × 置信度 × 市场波动环境
        
        Args:
            event: 结构化事件
            
        Returns:
            影响力分数 (0-1)
        """
        # 1. 事件类型重要性
        event_type = event.get('event_type', 'UNKNOWN')
        type_importance = self.config['event_types'].get(
            event_type, {}
        ).get('default_importance', 0.5)
        
        # 2. 因子相关度（取最强因子的强度）
        factor_tags = event.get('factor_tags', [])
        if factor_tags:
            max_strength = max([tag.get('strength', 0) for tag in factor_tags])
        else:
            max_strength = 0.5
        
        # 3. 置信度（取平均置信度）
        if factor_tags:
            avg_confidence = np.mean([tag.get('confidence', 0) for tag in factor_tags])
        else:
            avg_confidence = 0.5
        
        # 4. 市场环境（MVP: 固定为1，后续可以根据 VIX 等动态调整）
        market_volatility_multiplier = 1.0
        
        # 综合评分
        impact_score = type_importance * max_strength * avg_confidence * market_volatility_multiplier
        
        return round(impact_score, 3)
    
    def aggregate_factor_scores_by_day(self, events: List[Dict]) -> pd.DataFrame:
        """
        按天聚合因子分数
        
        Args:
            events: 事件列表
            
        Returns:
            DataFrame with columns: date, factor_code, score, event_count
        """
        records = []
        
        for event in events:
            # 解析事件时间
            timestamp = event.get('timestamp_utc', '')
            try:
                event_date = pd.to_datetime(timestamp).date()
            except:
                continue
            
            # 计算事件影响力
            impact_score = self.calculate_event_impact_score(event)
            
            # 提取因子标签
            for tag in event.get('factor_tags', []):
                factor_code = tag.get('factor', '')
                polarity = tag.get('polarity', '0')
                strength = tag.get('strength', 0)
                confidence = tag.get('confidence', 0)
                
                # 计算带极性的分数
                if polarity == '+':
                    signed_score = impact_score * strength
                elif polarity == '-':
                    signed_score = -impact_score * strength
                else:
                    signed_score = 0
                
                records.append({
                    'date': event_date,
                    'factor_code': factor_code,
                    'signed_score': signed_score,
                    'abs_score': abs(signed_score),
                    'event_id': event.get('event_id', '')
                })
        
        if not records:
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        
        # 按日期和因子聚合
        daily_factors = df.groupby(['date', 'factor_code']).agg({
            'signed_score': 'sum',  # 累计带符号分数
            'abs_score': 'sum',     # 累计绝对强度
            'event_id': 'count'     # 事件数量
        }).reset_index()
        
        daily_factors.columns = ['date', 'factor_code', 'score', 'intensity', 'event_count']
        
        return daily_factors
    
    def create_factor_timeseries(self, daily_factors: pd.DataFrame, 
                                  start_date: datetime, 
                                  end_date: datetime) -> pd.DataFrame:
        """
        创建完整的因子时间序列（填充缺失日期）
        
        Args:
            daily_factors: 按日聚合的因子数据
            start_date: 起始日期
            end_date: 结束日期
            
        Returns:
            完整的时间序列 DataFrame
        """
        if daily_factors.empty:
            return pd.DataFrame()
        
        # 获取所有因子代码
        all_factors = daily_factors['factor_code'].unique()
        
        # 创建完整日期范围
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 为每个因子创建完整时间序列
        full_series = []
        for factor in all_factors:
            factor_data = daily_factors[daily_factors['factor_code'] == factor].copy()
            factor_data['date'] = pd.to_datetime(factor_data['date'])
            factor_data = factor_data.set_index('date')

            # 只保留数值列用于 reindex
            numeric_cols = ['score', 'intensity', 'event_count']
            factor_data_numeric = factor_data[numeric_cols]

            # 重新索引到完整日期范围（只对数值列填充0）
            factor_data_numeric = factor_data_numeric.reindex(date_range, fill_value=0)

            # 添加因子代码列
            factor_data_numeric['factor_code'] = factor
            factor_data_numeric = factor_data_numeric.reset_index()
            factor_data_numeric.columns = ['date', 'score', 'intensity', 'event_count', 'factor_code']

            full_series.append(factor_data_numeric)
        
        result = pd.concat(full_series, ignore_index=True)
        result = result[['date', 'factor_code', 'score', 'intensity', 'event_count']]
        
        return result
    
    def align_with_price(self, factor_ts: pd.DataFrame, 
                         price_data: pd.DataFrame) -> pd.DataFrame:
        """
        将因子时间序列与价格数据对齐
        
        Args:
            factor_ts: 因子时间序列
            price_data: 价格数据 (包含 date, gold_price 列)
            
        Returns:
            对齐后的 DataFrame
        """
        if factor_ts.empty or price_data.empty:
            return pd.DataFrame()
        
        # 确保日期格式一致
        factor_ts['date'] = pd.to_datetime(factor_ts['date'])
        price_data['date'] = pd.to_datetime(price_data['date'])
        
        # 合并数据
        aligned = factor_ts.merge(
            price_data[['date', 'gold_price']], 
            on='date', 
            how='left'
        )
        
        # 前向填充价格（节假日无交易）
        aligned['gold_price'] = aligned['gold_price'].ffill()
        
        # 计算价格变化
        aligned['price_change_pct'] = aligned.groupby('factor_code')['gold_price'].pct_change() * 100
        
        return aligned
    
    def calculate_factor_influence_curve(self, aligned_data: pd.DataFrame, 
                                         window_days: int = 7) -> pd.DataFrame:
        """
        计算影响因素曲线（滚动窗口的因子强度归一化）
        
        这是系统的标志性功能：展示各因子随时间的解释权重变化
        
        Args:
            aligned_data: 对齐后的数据
            window_days: 滚动窗口大小
            
        Returns:
            影响曲线 DataFrame
        """
        if aligned_data.empty:
            return pd.DataFrame()
        
        # 按因子分组，计算滚动强度
        result = []
        
        for factor in aligned_data['factor_code'].unique():
            factor_data = aligned_data[aligned_data['factor_code'] == factor].copy()
            factor_data = factor_data.sort_values('date')
            
            # 滚动窗口累计强度
            factor_data['rolling_intensity'] = factor_data['intensity'].rolling(
                window=window_days, 
                min_periods=1
            ).sum()
            
            result.append(factor_data)
        
        combined = pd.concat(result, ignore_index=True)
        
        # 按日期归一化（每天所有因子的强度和为1）
        daily_totals = combined.groupby('date')['rolling_intensity'].transform('sum')
        combined['normalized_influence'] = combined['rolling_intensity'] / (daily_totals + 1e-6)
        
        # 选择关键列
        influence_curve = combined[[
            'date', 'factor_code', 'normalized_influence', 
            'rolling_intensity', 'score', 'gold_price'
        ]]
        
        return influence_curve
    
    def get_top_factors(self, influence_curve: pd.DataFrame, 
                        top_n: int = 5, 
                        recent_days: int = 7) -> List[Tuple[str, float]]:
        """
        获取最近N天最重要的因子
        
        Args:
            influence_curve: 影响曲线
            top_n: 返回前N个因子
            recent_days: 最近N天
            
        Returns:
            [(factor_code, avg_influence), ...]
        """
        if influence_curve.empty:
            return []
        
        # 筛选最近N天
        max_date = influence_curve['date'].max()
        cutoff_date = max_date - pd.Timedelta(days=recent_days)
        recent = influence_curve[influence_curve['date'] > cutoff_date]
        
        # 计算平均影响力
        factor_avg = recent.groupby('factor_code')['normalized_influence'].mean()
        factor_avg = factor_avg.sort_values(ascending=False)
        
        return list(factor_avg.head(top_n).items())
    
    def get_factor_name(self, factor_code: str) -> str:
        """获取因子的可读名称"""
        for domain in self.config['factor_domains'].values():
            if factor_code in domain['factors']:
                return domain['factors'][factor_code]['name']
        return factor_code


# 测试代码
if __name__ == "__main__":
    engine = FactorEngine()
    
    # 测试事件影响力计算
    sample_event = {
        'event_type': 'CENTRAL_BANK_DECISION',
        'factor_tags': [
            {'factor': 'A1_REAL_YIELD', 'polarity': '-', 'strength': 0.8, 'confidence': 0.9},
            {'factor': 'A2_POLICY_PATH', 'polarity': '+', 'strength': 0.7, 'confidence': 0.8}
        ]
    }
    
    score = engine.calculate_event_impact_score(sample_event)
    print(f"Event impact score: {score}")
    
    # 测试因子名称获取
    name = engine.get_factor_name('A1_REAL_YIELD')
    print(f"Factor name: {name}")
