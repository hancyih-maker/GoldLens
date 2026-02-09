# Gold Price Explainer 黄金价格解释器

一个基于 AI 的黄金价格分析系统，提供因子驱动的市场解读和可视化。

## 功能特点

- 📊 **实时价格跟踪**：黄金现货、美元指数、10年期实际收益率
- 📰 **智能新闻分析**：自动抽取事件、分类、归因到6大因子域
- 📈 **影响因素曲线**：可视化各因子对金价的解释权重变化
- 📝 **每日市场简报**：结构化的 Market Brief（Today in Gold）
- 🔍 **观察清单**：基于事件日历的前瞻性提醒

## 系统架构

```
数据层 (L0)
  ├─ 市场时间序列：金价、美元指数、实际收益率
  ├─ 新闻流：RSS/API 获取宏观新闻
  └─ 事件日历：CPI、FOMC、利率决议等

理解层 (L1-L2)
  ├─ 事件结构化抽取（Gemini API）
  ├─ 因子映射：6大超级域 × 细分因子
  └─ 影响强度评估

对齐层 (L3)
  ├─ 时间窗口分析（T-1 到 T+3）
  └─ 价格-事件共现模式

输出层 (L4)
  ├─ 每日 Market Brief
  ├─ 影响因素曲线可视化
  └─ 观察清单
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. 配置 API Keys

创建 `.env` 文件：

```env
GEMINI_API_KEY=your_gemini_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key  # 可选
NEWS_API_KEY=your_news_api_key  # 可选
```

### 3. 运行系统

```bash
# 数据采集和分析
python gold_analyzer.py

# 启动 Web 界面
python -m http.server 8000
# 访问 http://localhost:8000/dashboard.html
```

## 核心模块

- `gold_analyzer.py` - 主分析引擎
- `factor_engine.py` - 因子映射和评分系统
- `data_fetcher.py` - 数据获取模块
- `event_extractor.py` - 事件抽取（使用 Gemini）
- `factor_config.json` - 因子字典配置
- `dashboard.html` - 交互式可视化界面

## 6大因子域

1. **A) Monetary & Rates** - 货币政策与利率
2. **B) Inflation & Growth** - 通胀与增长
3. **C) FX & Liquidity** - 美元与流动性
4. **D) Risk & Geopolitics** - 风险偏好与地缘政治
5. **E) Physical Market** - 实物供需
6. **F) Market Microstructure** - 市场微观结构

## MVP 范围

当前版本聚焦于：
- ✅ 基础价格数据（金价、美元、利率）
- ✅ RSS/免费新闻源（每日20-50条）
- ✅ Gemini API 事件抽取
- ✅ 6大因子域基础映射
- ✅ 简单的每日简报
- ✅ 影响因素曲线可视化

## 技术栈

- **后端**：Python 3.8+
- **AI**：Google Gemini API
- **数据**：Alpha Vantage, Yahoo Finance, NewsAPI
- **可视化**：Chart.js, HTML/CSS/JS
- **存储**：JSON 文件（MVP）/ 可扩展至 SQLite

## 注意事项

⚠️ 本系统是**认知工具**，不是交易信号系统
⚠️ 所有分析基于历史模式和启发式规则
⚠️ 请结合专业金融建议使用

## License

MIT License
