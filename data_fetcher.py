"""
Data Fetcher Module
获取市场时间序列数据：黄金价格、美元指数、实际收益率等
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import os


class DataFetcher:
    """市场数据获取器"""
    
    def __init__(self, alpha_vantage_key: Optional[str] = None):
        self.av_key = alpha_vantage_key
        self.cache_dir = "data_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch_gold_price(self, days: int = 90) -> pd.DataFrame:
        """
        获取黄金现货价格 (XAU/USD)
        
        Args:
            days: 回溯天数
            
        Returns:
            DataFrame with columns: date, price, change_pct
        """
        try:
            # 使用 yfinance 获取黄金 ETF (GLD) 作为 proxy
            # 或者直接用 GC=F (黄金期货)
            ticker = yf.Ticker("GC=F")  # COMEX Gold Futures
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            df = pd.DataFrame({
                'date': hist.index,
                'price': hist['Close'].values,
                'volume': hist['Volume'].values
            })
            
            df['change_pct'] = df['price'].pct_change() * 100
            df = df.reset_index(drop=True)
            
            print(f"✓ Fetched {len(df)} days of gold price data")
            return df
            
        except Exception as e:
            print(f"✗ Error fetching gold price: {e}")
            return pd.DataFrame()
    
    def fetch_usd_index(self, days: int = 90) -> pd.DataFrame:
        """
        获取美元指数 (DXY)
        
        Args:
            days: 回溯天数
            
        Returns:
            DataFrame with columns: date, dxy, change_pct
        """
        try:
            ticker = yf.Ticker("DX-Y.NYB")  # US Dollar Index
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            df = pd.DataFrame({
                'date': hist.index,
                'dxy': hist['Close'].values
            })
            
            df['change_pct'] = df['dxy'].pct_change() * 100
            df = df.reset_index(drop=True)
            
            print(f"✓ Fetched {len(df)} days of USD index data")
            return df
            
        except Exception as e:
            print(f"✗ Error fetching USD index: {e}")
            return pd.DataFrame()
    
    def fetch_real_yield(self, days: int = 90) -> pd.DataFrame:
        """
        获取10年期实际收益率 (TIPS)
        使用 ^TYX (10-year Treasury) 作为 proxy
        
        Args:
            days: 回溯天数
            
        Returns:
            DataFrame with columns: date, yield, change_bps
        """
        try:
            # 使用 10-year Treasury yield as proxy
            # 真实的 TIPS 可以用 DFII (iShares TIPS ETF) 或者其他数据源
            ticker = yf.Ticker("^TNX")  # 10-Year Treasury Yield
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            df = pd.DataFrame({
                'date': hist.index,
                'yield': hist['Close'].values
            })
            
            df['change_bps'] = df['yield'].diff() * 100  # basis points
            df = df.reset_index(drop=True)
            
            print(f"✓ Fetched {len(df)} days of yield data")
            return df
            
        except Exception as e:
            print(f"✗ Error fetching real yield: {e}")
            return pd.DataFrame()
    
    def fetch_vix(self, days: int = 90) -> pd.DataFrame:
        """
        获取 VIX 波动率指数（风险情绪代理）
        
        Args:
            days: 回溯天数
            
        Returns:
            DataFrame with columns: date, vix
        """
        try:
            ticker = yf.Ticker("^VIX")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            df = pd.DataFrame({
                'date': hist.index,
                'vix': hist['Close'].values
            })
            df = df.reset_index(drop=True)
            
            print(f"✓ Fetched {len(df)} days of VIX data")
            return df
            
        except Exception as e:
            print(f"✗ Error fetching VIX: {e}")
            return pd.DataFrame()
    
    def fetch_all_market_data(self, days: int = 90) -> Dict[str, pd.DataFrame]:
        """
        获取所有市场数据
        
        Args:
            days: 回溯天数
            
        Returns:
            Dictionary of DataFrames
        """
        print(f"\n📊 Fetching market data for last {days} days...\n")
        
        data = {
            'gold': self.fetch_gold_price(days),
            'usd': self.fetch_usd_index(days),
            'yield': self.fetch_real_yield(days),
            'vix': self.fetch_vix(days)
        }
        
        # 保存到缓存
        cache_file = os.path.join(self.cache_dir, f"market_data_{datetime.now().strftime('%Y%m%d')}.json")
        
        # Convert to JSON-serializable format
        cache_data = {}
        for key, df in data.items():
            if not df.empty:
                df_copy = df.copy()
                df_copy['date'] = df_copy['date'].astype(str)
                cache_data[key] = df_copy.to_dict('records')
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"\n✓ Market data cached to {cache_file}")
        
        return data
    
    def align_data(self, data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        对齐所有数据到同一时间轴
        
        Args:
            data_dict: Dictionary of DataFrames
            
        Returns:
            Aligned DataFrame
        """
        if not data_dict or all(df.empty for df in data_dict.values()):
            return pd.DataFrame()
        
        # 以黄金价格为基准
        base_df = data_dict['gold'][['date', 'price']].copy()
        base_df.columns = ['date', 'gold_price']
        
        # 逐个合并其他数据
        if not data_dict['usd'].empty:
            base_df = base_df.merge(
                data_dict['usd'][['date', 'dxy']], 
                on='date', 
                how='left'
            )
        
        if not data_dict['yield'].empty:
            base_df = base_df.merge(
                data_dict['yield'][['date', 'yield']], 
                on='date', 
                how='left'
            )
        
        if not data_dict['vix'].empty:
            base_df = base_df.merge(
                data_dict['vix'][['date', 'vix']], 
                on='date', 
                how='left'
            )
        
        # 前向填充缺失值
        base_df = base_df.ffill()
        
        print(f"\n✓ Aligned data: {len(base_df)} rows")
        return base_df


# 测试代码
if __name__ == "__main__":
    fetcher = DataFetcher()
    
    # 获取所有数据
    data = fetcher.fetch_all_market_data(days=30)
    
    # 对齐数据
    aligned = fetcher.align_data(data)
    
    if not aligned.empty:
        print("\n📈 Sample of aligned data:")
        print(aligned.tail())
        
        print(f"\n📊 Latest values:")
        latest = aligned.iloc[-1]
        print(f"Gold Price: ${latest['gold_price']:.2f}")
        if 'dxy' in latest:
            print(f"USD Index: {latest['dxy']:.2f}")
        if 'yield' in latest:
            print(f"10Y Yield: {latest['yield']:.2f}%")
        if 'vix' in latest:
            print(f"VIX: {latest['vix']:.2f}")
