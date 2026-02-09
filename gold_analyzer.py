"""
Gold Analyzer - Main Analysis Engine
黄金价格解释器主程序
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

from data_fetcher import DataFetcher
from news_fetcher import NewsFetcher
from event_extractor import EventExtractor
from factor_engine import FactorEngine


class GoldAnalyzer:
    """黄金价格分析器"""
    
    def __init__(self, gemini_api_key: str, 
                 news_api_key: str = None,
                 alpha_vantage_key: str = None):
        """
        初始化分析器
        
        Args:
            gemini_api_key: Gemini API key (必需)
            news_api_key: NewsAPI key (可选)
            alpha_vantage_key: Alpha Vantage key (可选)
        """
        self.data_fetcher = DataFetcher(alpha_vantage_key)
        self.news_fetcher = NewsFetcher(news_api_key)
        self.event_extractor = EventExtractor(gemini_api_key)
        self.factor_engine = FactorEngine()
        
        self.output_dir = "analysis_output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_full_analysis(self, days_back: int = 30, 
                          max_news: int = 50) -> Dict:
        """
        运行完整分析流程
        
        Args:
            days_back: 回溯天数
            max_news: 最多处理多少条新闻
            
        Returns:
            分析结果字典
        """
        print("=" * 60)
        print("🏆 GOLD PRICE EXPLAINER - FULL ANALYSIS")
        print("=" * 60)
        
        # Step 1: 获取市场数据
        print("\n📊 STEP 1: Fetching Market Data")
        print("-" * 60)
        market_data = self.data_fetcher.fetch_all_market_data(days=days_back)
        aligned_prices = self.data_fetcher.align_data(market_data)
        
        if aligned_prices.empty:
            print("❌ Failed to fetch market data")
            return {}
        
        # Step 2: 获取新闻
        print("\n📰 STEP 2: Fetching News")
        print("-" * 60)
        news_list = self.news_fetcher.fetch_all_news(max_age_hours=days_back*24)
        
        if not news_list:
            print("❌ No news fetched")
            return {}
        
        # Step 3: 事件抽取
        print("\n🤖 STEP 3: Extracting Events (using Gemini API)")
        print("-" * 60)
        events = self.event_extractor.batch_extract(news_list, max_items=max_news)
        
        if not events:
            print("❌ No events extracted")
            return {}
        
        # 保存事件
        events_file = self.event_extractor.save_events(events, self.output_dir)
        
        # Step 4: 因子分析
        print("\n📈 STEP 4: Factor Analysis")
        print("-" * 60)
        
        # 聚合因子分数
        daily_factors = self.factor_engine.aggregate_factor_scores_by_day(events)
        print(f"✓ Aggregated {len(daily_factors)} factor-day combinations")
        
        # 创建完整时间序列
        start_date = aligned_prices['date'].min()
        end_date = aligned_prices['date'].max()
        factor_ts = self.factor_engine.create_factor_timeseries(
            daily_factors, start_date, end_date
        )
        print(f"✓ Created complete time series")
        
        # 与价格对齐
        aligned_data = self.factor_engine.align_with_price(factor_ts, aligned_prices)
        print(f"✓ Aligned with price data: {len(aligned_data)} records")
        
        # 计算影响曲线
        influence_curve = self.factor_engine.calculate_factor_influence_curve(
            aligned_data, window_days=7
        )
        print(f"✓ Calculated influence curve")
        
        # Step 5: 生成每日简报
        print("\n📝 STEP 5: Generating Daily Brief")
        print("-" * 60)
        daily_brief = self.generate_daily_brief(
            events, aligned_prices, influence_curve
        )
        
        # 保存所有结果
        results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'daily_brief': daily_brief,
            'events': events,
            'market_data': aligned_prices.assign(date=aligned_prices['date'].dt.strftime('%Y-%m-%d')).to_dict('records'),
            'influence_curve': influence_curve.assign(date=influence_curve['date'].dt.strftime('%Y-%m-%d')).to_dict('records'),
            'top_factors': self.factor_engine.get_top_factors(influence_curve, top_n=5)
        }
        
        output_file = os.path.join(
            self.output_dir, 
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Full analysis saved to {output_file}")
        
        # 打印简报
        self.print_brief(daily_brief)
        
        return results
    
    def generate_daily_brief(self, events: List[Dict], 
                            price_data: pd.DataFrame,
                            influence_curve: pd.DataFrame) -> Dict:
        """
        生成每日市场简报 (Today in Gold)
        
        Args:
            events: 事件列表
            price_data: 价格数据
            influence_curve: 影响曲线
            
        Returns:
            简报字典
        """
        # 最新价格快照
        latest = price_data.iloc[-1]
        prev = price_data.iloc[-2] if len(price_data) > 1 else latest
        
        price_snapshot = {
            'date': str(latest['date']),
            'gold_price': round(float(latest['gold_price']), 2),
            'change_pct': round(float((latest['gold_price'] - prev['gold_price']) / prev['gold_price'] * 100), 2),
            'dxy': round(float(latest.get('dxy', 0)), 2) if 'dxy' in latest else None,
            'yield': round(float(latest.get('yield', 0)), 2) if 'yield' in latest else None,
            'vix': round(float(latest.get('vix', 0)), 2) if 'vix' in latest else None
        }
        
        # What happened - 最近的重要事件（按影响力排序）
        recent_events = sorted(
            events, 
            key=lambda e: self.factor_engine.calculate_event_impact_score(e),
            reverse=True
        )[:5]
        
        what_happened = [
            {
                'headline': e['headline'],
                'event_type': e['event_type'],
                'impact_score': self.factor_engine.calculate_event_impact_score(e),
                'factors': [tag['factor'] for tag in e.get('factor_tags', [])]
            }
            for e in recent_events
        ]
        
        # Why it may matter - 按因子分组
        top_factors = self.factor_engine.get_top_factors(influence_curve, top_n=3, recent_days=7)
        
        why_matters = []
        for factor_code, influence in top_factors:
            factor_name = self.factor_engine.get_factor_name(factor_code)
            
            # 找到该因子相关的事件
            related_events = [
                e for e in recent_events 
                if any(tag['factor'] == factor_code for tag in e.get('factor_tags', []))
            ]
            
            why_matters.append({
                'factor_code': factor_code,
                'factor_name': factor_name,
                'influence_score': round(influence, 3),
                'event_count': len(related_events),
                'sample_event': related_events[0]['headline'] if related_events else None
            })
        
        # What to watch next - 从日历事件获取
        calendar_events = self.news_fetcher.get_calendar_events()
        watch_next = calendar_events[:3]  # MVP: 固定列表
        
        brief = {
            'title': 'Today in Gold',
            'date': str(latest['date']),
            'price_snapshot': price_snapshot,
            'what_happened': what_happened,
            'why_matters': why_matters,
            'watch_next': watch_next
        }
        
        return brief
    
    def print_brief(self, brief: Dict):
        """打印每日简报到控制台"""
        print("\n" + "=" * 60)
        print(f"📊 {brief['title']} - {brief['date']}")
        print("=" * 60)
        
        # Price Snapshot
        ps = brief['price_snapshot']
        print(f"\n💰 PRICE SNAPSHOT")
        print(f"   Gold: ${ps['gold_price']} ({ps['change_pct']:+.2f}%)")
        if ps['dxy']:
            print(f"   USD Index: {ps['dxy']}")
        if ps['yield']:
            print(f"   10Y Yield: {ps['yield']}%")
        if ps['vix']:
            print(f"   VIX: {ps['vix']}")
        
        # What Happened
        print(f"\n📰 WHAT HAPPENED (Top 3)")
        for i, event in enumerate(brief['what_happened'][:3], 1):
            print(f"   {i}. {event['headline'][:70]}")
            print(f"      Impact: {event['impact_score']:.2f} | Factors: {', '.join(event['factors'][:2])}")
        
        # Why It Matters
        print(f"\n🎯 WHY IT MAY MATTER")
        for item in brief['why_matters']:
            print(f"   • {item['factor_name']}")
            print(f"     Influence: {item['influence_score']:.1%} | Events: {item['event_count']}")
            if item['sample_event']:
                print(f"     Example: {item['sample_event'][:60]}")
        
        # What to Watch
        print(f"\n👀 WHAT TO WATCH NEXT")
        for event in brief['watch_next']:
            print(f"   • {event['name']} ({event['schedule']})")
        
        print("\n" + "=" * 60)


# Main execution
if __name__ == "__main__":
    # 从环境变量读取 API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    av_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not gemini_key:
        print("❌ Please set GEMINI_API_KEY in .env file or environment")
        print("\nCreate a .env file with:")
        print("GEMINI_API_KEY=your_key_here")
        print("NEWS_API_KEY=your_key_here  # optional")
        exit(1)
    
    # 运行分析
    analyzer = GoldAnalyzer(
        gemini_api_key=gemini_key,
        news_api_key=news_key,
        alpha_vantage_key=av_key
    )
    
    results = analyzer.run_full_analysis(days_back=30, max_news=30)
    
    if results:
        print("\n✅ Analysis complete!")
        print(f"   Results saved to: analysis_output/")
        print(f"   You can now open dashboard.html to view visualizations")
