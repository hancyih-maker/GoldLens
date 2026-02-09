"""
Event Extractor Module
使用 Gemini API 进行事件结构化抽取和因子映射
"""

import google.generativeai as genai
import json
from typing import Dict, List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

class EventExtractor:
    """使用 Gemini API 的事件抽取器"""
    
    def __init__(self, api_key: str, factor_config_path: str = "factor_config.json"):
        """
        初始化事件抽取器
        
        Args:
            api_key: Gemini API key
            factor_config_path: 因子配置文件路径
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 加载因子配置
        with open(factor_config_path, 'r', encoding='utf-8') as f:
            self.factor_config = json.load(f)
        
        self.extraction_prompt = self._build_extraction_prompt()
    
    def _build_extraction_prompt(self) -> str:
        """构建事件抽取的提示词"""
        
        # 提取因子列表
        factor_list = []
        for domain_key, domain in self.factor_config['factor_domains'].items():
            for factor_key, factor in domain['factors'].items():
                factor_list.append(f"- {factor_key}: {factor['name']}")
        
        prompt = f"""You are an expert financial analyst specializing in gold market analysis.

Your task is to extract structured information from news articles and classify them according to the gold price factor framework.

**FACTOR FRAMEWORK:**
{chr(10).join(factor_list)}

**EVENT TYPES:**
- MACRO_DATA_RELEASE (CPI, PCE, GDP, PMI, Jobs)
- CENTRAL_BANK_SPEECH (Fed, ECB, BOJ speeches)
- CENTRAL_BANK_DECISION (Rate decisions, QE/QT)
- GEOPOLITICAL_ESCALATION (Wars, conflicts, tensions)
- SANCTIONS (Financial restrictions, trade measures)
- ETF_FLOW (Gold ETF inflows/outflows)
- MINING_DISRUPTION (Mine strikes, closures)
- POLICY_ANNOUNCEMENT (Fiscal, regulatory policies)

**ACTORS:**
Central banks: Fed, ECB, BOJ, BOE, PBoC, RBI
Governments: US Treasury, China, Russia, India
Organizations: IMF, World Bank, WGC, OPEC

**YOUR OUTPUT MUST BE VALID JSON** in this exact format:
{{
  "event_type": "EVENT_TYPE",
  "actors": ["Actor1", "Actor2"],
  "stance": "Hawkish/Dovish/Neutral/Risk-off/Risk-on",
  "topic": ["Topic1", "Topic2"],
  "sentiment": "Risk-off/Risk-on/Neutral",
  "factor_tags": [
    {{"factor": "FACTOR_CODE", "polarity": "+/-/0", "strength": 0.0-1.0, "confidence": 0.0-1.0}}
  ],
  "mechanism_path": ["FACTOR1 -> FACTOR2 -> GOLD_PRICE"],
  "horizon": "INTRADAY/1-3D/1-4W/1-6M",
  "uncertainty_notes": ["Note1", "Note2"],
  "evidence_quotes": ["Short quote 1", "Short quote 2"]
}}

**RULES:**
1. Assign 1-3 most relevant factors (not all factors)
2. Polarity: "+" = bullish for gold, "-" = bearish, "0" = unclear
3. Strength: 0.0-1.0 (how strong this factor is activated)
4. Confidence: 0.0-1.0 (your confidence in the assessment)
5. Be conservative - if unclear, use lower scores
6. Focus on direct gold market relevance

Return ONLY the JSON object, no other text.
"""
        return prompt
    
    def extract_event(self, news_item: Dict) -> Optional[Dict]:
        """
        从单条新闻中抽取结构化事件
        
        Args:
            news_item: 新闻字典 (含 title, summary, url 等)
            
        Returns:
            结构化事件字典，或 None（如果抽取失败）
        """
        try:
            # 构建输入文本
            input_text = f"""
NEWS ARTICLE:
Title: {news_item.get('title', '')}
Summary: {news_item.get('summary', '')}
Source: {news_item.get('source', '')}
Published: {news_item.get('published', '')}

Analyze this article and extract structured event information.
"""
            
            # 调用 Gemini API
            full_prompt = self.extraction_prompt + "\n\n" + input_text
            response = self.model.generate_content(full_prompt)
            
            # 解析 JSON 响应
            response_text = response.text.strip()
            
            # 移除可能的 markdown 代码块标记
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            event = json.loads(response_text.strip())
            
            # 添加元数据
            event['event_id'] = f"evt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(news_item.get('url', '')) % 10000}"
            event['timestamp_utc'] = news_item.get('published', datetime.now().isoformat())
            event['source'] = {
                'publisher': news_item.get('source', ''),
                'url': news_item.get('url', ''),
                'credibility_tier': 1  # MVP: 默认值，可以后续优化
            }
            event['headline'] = news_item.get('title', '')
            event['summary'] = news_item.get('summary', '')[:500]  # 截断
            
            return event
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {e}")
            print(f"  Response: {response_text[:200]}...")
            return None
        except Exception as e:
            print(f"✗ Error extracting event: {e}")
            return None
    
    def batch_extract(self, news_list: List[Dict], max_items: int = 50) -> List[Dict]:
        """
        批量抽取事件
        
        Args:
            news_list: 新闻列表
            max_items: 最多处理多少条（控制 API 成本）
            
        Returns:
            事件列表
        """
        events = []
        
        print(f"\n🤖 Extracting events using Gemini API...")
        print(f"   Processing up to {min(len(news_list), max_items)} articles\n")
        
        for i, news_item in enumerate(news_list[:max_items], 1):
            print(f"[{i}/{min(len(news_list), max_items)}] {news_item.get('title', '')[:60]}...")
            
            event = self.extract_event(news_item)
            
            if event:
                events.append(event)
                print(f"  ✓ Event type: {event.get('event_type', 'N/A')}")
                print(f"  ✓ Factors: {', '.join([f['factor'] for f in event.get('factor_tags', [])])}")
            else:
                print(f"  ✗ Failed to extract")
            
            print()
        
        print(f"✓ Extracted {len(events)} events from {min(len(news_list), max_items)} articles")
        
        return events
    
    def save_events(self, events: List[Dict], output_dir: str = "events_output"):
        """
        保存事件到文件
        
        Args:
            events: 事件列表
            output_dir: 输出目录
        """
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Events saved to {filepath}")
        return filepath

load_dotenv()

# 测试代码
if __name__ == "__main__":
    # 需要设置环境变量 GEMINI_API_KEY
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        exit(1)
    
    extractor = EventExtractor(api_key)
    
    # 测试样本
    sample_news = [
        {
            'title': 'Fed Holds Rates Steady, Signals Caution on Inflation',
            'summary': 'The Federal Reserve kept interest rates unchanged at 5.25-5.5% and indicated it needs to see more progress on inflation before considering rate cuts.',
            'source': 'Reuters',
            'published': '2024-01-31T14:00:00Z',
            'url': 'https://example.com/fed-rates'
        },
        {
            'title': 'Gold Prices Rise on Geopolitical Tensions in Middle East',
            'summary': 'Gold futures climbed 1.2% as escalating tensions in the Middle East drove safe-haven demand.',
            'source': 'Bloomberg',
            'published': '2024-01-31T10:30:00Z',
            'url': 'https://example.com/gold-rises'
        }
    ]
    
    events = extractor.batch_extract(sample_news)
    
    if events:
        extractor.save_events(events)
        
        print("\n📋 Sample extracted event:")
        print(json.dumps(events[0], indent=2))
