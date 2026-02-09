"""
News Fetcher Module
获取黄金相关的宏观新闻（RSS feeds + NewsAPI）
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os


class NewsFetcher:
    """新闻获取器"""
    
    # 免费的 RSS 源（聚焦于宏观经济、央行、地缘政治）
    RSS_FEEDS = [
        # 央行与货币政策
        "https://www.federalreserve.gov/feeds/press_all.xml",
        "https://www.ecb.europa.eu/rss/press.html",
        
        # 金融新闻
        "https://www.reuters.com/finance/markets/feed/",
        "https://feeds.bloomberg.com/markets/news.rss",
        
        # 黄金专门
        "https://www.kitco.com/rss/KitcoNews.xml",
        "https://www.mining.com/rss/",
        
        # 宏观经济
        "https://www.imf.org/en/News/RSS",
    ]
    
    # 关键词过滤（只保留与黄金相关的新闻）
    GOLD_KEYWORDS = [
        'gold', 'xau', 'precious metal', 'bullion',
        'federal reserve', 'fed', 'interest rate', 'inflation',
        'dollar', 'dxy', 'treasury', 'yield',
        'geopolitical', 'war', 'sanction', 'crisis',
        'central bank', 'monetary policy', 'ecb', 'boj'
    ]
    
    def __init__(self, news_api_key: Optional[str] = None):
        self.news_api_key = news_api_key
        self.cache_dir = "news_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def fetch_from_rss(self, max_age_hours: int = 48) -> List[Dict]:
        """
        从 RSS feeds 获取新闻
        
        Args:
            max_age_hours: 只获取最近N小时的新闻
            
        Returns:
            List of news items
        """
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        print(f"\n📰 Fetching news from {len(self.RSS_FEEDS)} RSS feeds...")
        
        for feed_url in self.RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                source = feed.feed.get('title', feed_url)
                
                for entry in feed.entries[:20]:  # 每个源最多取20条
                    # 解析时间
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])
                    
                    # 检查时间范围
                    if pub_date and pub_date < cutoff_time:
                        continue
                    
                    # 提取内容
                    title = entry.get('title', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    link = entry.get('link', '')
                    
                    # 关键词过滤
                    content = (title + ' ' + summary).lower()
                    if not any(kw in content for kw in self.GOLD_KEYWORDS):
                        continue
                    
                    all_news.append({
                        'source': source,
                        'title': title,
                        'summary': summary,
                        'url': link,
                        'published': pub_date.isoformat() if pub_date else None,
                        'fetched_at': datetime.now().isoformat()
                    })
                
                print(f"  ✓ {source}: {len([n for n in all_news if n['source'] == source])} articles")
                
            except Exception as e:
                print(f"  ✗ Error fetching {feed_url}: {e}")
        
        print(f"\n✓ Total fetched: {len(all_news)} relevant articles")
        return all_news
    
    def fetch_from_newsapi(self, query: str = "gold OR inflation OR federal reserve", 
                           days: int = 2) -> List[Dict]:
        """
        从 NewsAPI 获取新闻（需要 API key）
        
        Args:
            query: 搜索查询
            days: 回溯天数
            
        Returns:
            List of news items
        """
        if not self.news_api_key:
            print("⚠ NewsAPI key not provided, skipping NewsAPI")
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': self.news_api_key,
                'pageSize': 50
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            news_items = []
            for article in articles:
                news_items.append({
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'title': article.get('title', ''),
                    'summary': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published': article.get('publishedAt', None),
                    'fetched_at': datetime.now().isoformat()
                })
            
            print(f"✓ NewsAPI: {len(news_items)} articles")
            return news_items
            
        except Exception as e:
            print(f"✗ Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_all_news(self, max_age_hours: int = 48) -> List[Dict]:
        """
        获取所有新闻源
        
        Args:
            max_age_hours: 最近N小时
            
        Returns:
            Combined list of news items
        """
        all_news = []
        
        # RSS feeds
        rss_news = self.fetch_from_rss(max_age_hours)
        all_news.extend(rss_news)
        
        # NewsAPI (如果有 key)
        if self.news_api_key:
            api_news = self.fetch_from_newsapi(days=max_age_hours//24 + 1)
            all_news.extend(api_news)
        
        # 去重（基于 URL）
        seen_urls = set()
        unique_news = []
        for item in all_news:
            url = item.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(item)
        
        # 按时间排序
        unique_news.sort(
            key=lambda x: x.get('published', ''), 
            reverse=True
        )
        
        # 保存到缓存
        cache_file = os.path.join(
            self.cache_dir, 
            f"news_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(unique_news, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Total unique articles: {len(unique_news)}")
        print(f"✓ Cached to {cache_file}")
        
        return unique_news
    
    def get_calendar_events(self) -> List[Dict]:
        """
        获取经济日历事件（MVP: 硬编码常见事件）
        在生产环境中可以接入 Trading Economics API 等
        
        Returns:
            List of calendar events
        """
        # MVP: 返回常见的周期性事件
        # 真实实现需要从 API 获取
        events = [
            {
                'event_type': 'MACRO_DATA_RELEASE',
                'name': 'US CPI',
                'schedule': 'Monthly, ~13th',
                'impact': 'High',
                'next_date': None  # 需要实时 API
            },
            {
                'event_type': 'MACRO_DATA_RELEASE',
                'name': 'US PCE',
                'schedule': 'Monthly, end of month',
                'impact': 'High',
                'next_date': None
            },
            {
                'event_type': 'CENTRAL_BANK_DECISION',
                'name': 'FOMC Meeting',
                'schedule': '~8 times per year',
                'impact': 'Very High',
                'next_date': None
            },
            {
                'event_type': 'MACRO_DATA_RELEASE',
                'name': 'US Jobs Report',
                'schedule': 'First Friday of month',
                'impact': 'High',
                'next_date': None
            }
        ]
        
        return events


# 测试代码
if __name__ == "__main__":
    # 从环境变量读取 API key（可选）
    news_api_key = os.getenv('NEWS_API_KEY')
    
    fetcher = NewsFetcher(news_api_key=news_api_key)
    
    # 获取新闻
    news = fetcher.fetch_all_news(max_age_hours=72)
    
    if news:
        print("\n📄 Sample news items:")
        for item in news[:5]:
            print(f"\n- {item['title']}")
            print(f"  Source: {item['source']}")
            print(f"  Published: {item['published']}")
    
    # 获取日历事件
    calendar = fetcher.get_calendar_events()
    print(f"\n📅 Calendar events: {len(calendar)} items")
