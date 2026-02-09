# 🏆 Gold Price Explainer - Quick Start Guide

## Overview

This is an AI-powered **Gold Price Explainer** system that can:

* Automatically fetch market data (gold price, USD index, yields, etc.)
* Collect and analyse financial news
* Use the **Gemini API** to extract **structured market events**
* Map events into **six factor domains** (monetary policy, inflation, USD, geopolitics, physical market, microstructure)
* Generate a daily market brief (**Today in Gold**)
* Visualise **impact factor curves**

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

Main dependencies:

* `google-generativeai` - Gemini API
* `yfinance` - free market data
* `feedparser` - RSS news ingestion
* `pandas`, `numpy` - data processing

### 2. Configure API Keys

Create a `.env` file (copy from the template):

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_actual_gemini_key
# Other keys are optional
```

**Get a Gemini API Key:**

1. Visit [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create an API key
4. Paste it into your `.env` file

## Running the System

### Option 1: Full analysis (recommended)

```bash
python gold_analyzer.py
```

This will:

1. Fetch the last 30 days of market data
2. Collect relevant news (via RSS feeds)
3. Use Gemini to extract events (up to 30 items by default to control cost)
4. Analyse factor influence
5. Generate the daily brief
6. Save outputs to `analysis_output/`

**Expected output:**

```
📊 STEP 1: Fetching Market Data
✓ Fetched 30 days of gold price data
✓ Fetched 30 days of USD index data
...

📰 STEP 2: Fetching News
✓ Total fetched: 45 relevant articles

🤖 STEP 3: Extracting Events (using Gemini API)
[1/30] Fed Holds Rates Steady...
  ✓ Event type: CENTRAL_BANK_DECISION
  ✓ Factors: A1_REAL_YIELD, A2_POLICY_PATH
...

📝 STEP 5: Generating Daily Brief
...
```

### Option 2: Test modules individually

```bash
# Test market data fetching
python data_fetcher.py

# Test news fetching
python news_fetcher.py

# Test event extraction (requires news data first)
python event_extractor.py
```

## Viewing Visualisations

### 1. Open the Dashboard

```bash
# Start a local server
python -m http.server 8000
```

### 2. Visit in your browser

```
http://localhost:8000/dashboard.html
```

### 3. Load analysis results

1. Click **"Load Analysis Results"**
2. Select the latest JSON file under `analysis_output/`
3. Explore:

   * Price snapshot (Gold, USD, Yield, VIX)
   * What Happened (top 5 events)
   * Why It Matters (top 3 active factors)
   * What to Watch Next (upcoming macro events)
   * Gold vs USD trend charts
   * **Impact Factor Curves** (core feature)

## Core Features Explained

### 1. Impact Factor Curves

This is the signature feature. It shows:

* **X-axis**: time
* **Y-axis**: normalised factor influence (0–1)
* **Meaning**: which factors are most dominant in explaining the gold narrative over time

**Example interpretations:**

* If **A1_REAL_YIELD** (real yields) rises → rate-related drivers have become more influential recently
* If **D1_GEOPOLITICAL** spikes → geopolitical events have become the dominant narrative

**This is not a prediction tool — it is narrative visualisation.**

### 2. Daily Brief Structure

```
Today in Gold - 2024-01-31

💰 PRICE SNAPSHOT
   Gold: $2043.50 (+0.45%)
   USD Index: 103.25
   10Y Yield: 4.12%

📰 WHAT HAPPENED (Top 3)
   1. Fed Holds Rates Steady...
   2. Middle East Tensions Rise...
   3. ETF Inflows Continue...

🎯 WHY IT MAY MATTER
   • Real Yields
     Influence: 35.2% | Events: 3
   • Geopolitical Conflict
     Influence: 28.7% | Events: 2

👀 WHAT TO WATCH NEXT
   • US CPI (Monthly, ~13th)
   • FOMC Meeting (~8 times per year)
```

### 3. The Six Factor Domains

All extracted events are mapped into these factor domains:

**A) Monetary & Rates**

* A1_REAL_YIELD: real yields
* A2_POLICY_PATH: policy path expectations
* A3_QE_QT: QE/QT and financial stability

**B) Inflation & Growth**

* B1_INFLATION: inflation level and surprise
* B2_RECESSION_RISK: recession risk

**C) FX & Liquidity**

* C1_USD_STRENGTH: USD strength
* C2_LIQUIDITY: global liquidity

**D) Risk & Geopolitics**

* D1_GEOPOLITICAL: geopolitical conflict
* D2_SANCTIONS: sanctions and reserve diversification
* D3_POLITICAL_RISK: political risk

**E) Physical Market**

* E1_CENTRAL_BANK: central bank gold buying
* E2_ETF_FLOWS: ETF flows
* E3_JEWELRY: jewellery demand
* E5_SUPPLY: supply shocks

**F) Market Microstructure**

* F1_POSITIONING: futures positioning
* F2_TERM_STRUCTURE: term structure

## Cost Control

### Gemini API Usage

* **Free quota**: ~60 requests per day
* **Typical usage**: ~30–50 requests per full run (processing 30–50 news items)
* **Recommendations**:

  * Run a full analysis once per day
  * Reduce processing volume by lowering `max_news`

```python
# Adjust in gold_analyzer.py
results = analyzer.run_full_analysis(
    days_back=30,    # lookback window
    max_news=20      # reduce to 20 to cut API calls
)
```

## Troubleshooting

### Issue 1: No news fetched

**Cause**: RSS feeds may be temporarily unavailable
**Fix**:

* Check your internet connection
* Retry after a few minutes
* Or provide a NewsAPI key

### Issue 2: Gemini API error

**Cause**: invalid API key or quota exceeded
**Fix**:

* Verify the key in `.env`
* Check quota at [https://makersuite.google.com/](https://makersuite.google.com/)
* Reduce the `max_news` parameter

### Issue 3: Empty chart

**Cause**: results not loaded correctly
**Fix**:

* Ensure you ran `python gold_analyzer.py`
* Confirm `analysis_output/` contains JSON outputs
* Upload the correct file in the dashboard

## Next Improvements

This is an MVP. Possible extensions include:

1. **Data Layer**

   * Integrate paid data sources (Bloomberg, Refinitiv)
   * Add real-time ETF holdings tracking
   * Use an economic calendar API

2. **Understanding Layer**

   * Fine-tune or calibrate extraction for higher accuracy
   * Add sentiment analysis
   * Support multilingual news

3. **Alignment Layer**

   * More advanced causal inference methods
   * ML-based forecasting (carefully!)
   * Better event-window optimisation

4. **Output Layer**

   * Auto-generate reports (PDF/PPT)
   * Email / Slack delivery
   * Mobile app

5. **Storage**

   * Migrate from JSON to SQLite/PostgreSQL
   * Add historical data management
   * Implement incremental updates

## Project Structure

```
gold-price-explainer/
├── README.md                    # project overview
├── QUICKSTART.md               # this file
├── requirements.txt            # Python dependencies
├── .env.example                # environment template
├── factor_config.json          # factor dictionary (core)
├── gold_analyzer.py            # main entry point
├── data_fetcher.py             # market data fetcher
├── news_fetcher.py             # news ingestion
├── event_extractor.py          # event extraction (Gemini)
├── factor_engine.py            # factor analytics
├── dashboard.html              # visual UI
├── data_cache/                 # market data cache
├── news_cache/                 # news cache
├── events_output/              # extracted events
└── analysis_output/            # analysis results
```

## Contact & Feedback

This is an open-source project template. You’re welcome to:

* Open Issues to report bugs
* Submit PRs to contribute
* Fork the project and customise it

**Important reminder:**
⚠️ This system is a **research and interpretation tool**, not a trading signal.
⚠️ All analysis is based on historical patterns and heuristic scoring, not investment advice.
⚠️ Please use alongside professional financial guidance.

Enjoy! 🚀


# 🏆 Gold Price Explainer - Quick Start Guide

## 简介

这是一个基于 AI 的黄金价格解释器系统，能够：
- 自动获取市场数据（金价、美元指数、利率等）
- 抓取和分析金融新闻
- 使用 Gemini API 进行事件结构化抽取
- 将事件映射到 6 大因子域（货币政策、通胀、美元、地缘、实物市场、市场微观）
- 生成每日市场简报（Today in Gold）
- 可视化影响因素曲线

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt --break-system-packages
```

主要依赖：
- `google-generativeai` - Gemini API
- `yfinance` - 免费金融数据
- `feedparser` - RSS 新闻抓取
- `pandas`, `numpy` - 数据处理

### 2. 配置 API Keys

创建 `.env` 文件（从模板复制）：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API keys：

```env
GEMINI_API_KEY=your_actual_gemini_key
# 其他 keys 可选
```

**获取 Gemini API Key：**
1. 访问 https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 创建 API key
4. 复制到 `.env` 文件

## 运行系统

### 方法 1：完整分析（推荐）

```bash
python gold_analyzer.py
```

这将：
1. 获取最近 30 天的市场数据
2. 抓取相关新闻（RSS feeds）
3. 使用 Gemini 抽取事件（最多 30 条，可控制成本）
4. 分析因子影响
5. 生成每日简报
6. 保存结果到 `analysis_output/`

**预期输出：**
```
📊 STEP 1: Fetching Market Data
✓ Fetched 30 days of gold price data
✓ Fetched 30 days of USD index data
...

📰 STEP 2: Fetching News
✓ Total fetched: 45 relevant articles

🤖 STEP 3: Extracting Events (using Gemini API)
[1/30] Fed Holds Rates Steady...
  ✓ Event type: CENTRAL_BANK_DECISION
  ✓ Factors: A1_REAL_YIELD, A2_POLICY_PATH
...

📝 STEP 5: Generating Daily Brief
...
```

### 方法 2：单独测试各模块

```bash
# 测试数据获取
python data_fetcher.py

# 测试新闻抓取
python news_fetcher.py

# 测试事件抽取（需要先有新闻数据）
python event_extractor.py
```

## 查看可视化

### 1. 打开 Dashboard

```bash
# 启动本地服务器
python -m http.server 8000
```

### 2. 在浏览器访问

```
http://localhost:8000/dashboard.html
```

### 3. 加载分析结果

1. 点击"Load Analysis Results"
2. 选择 `analysis_output/` 目录下最新的 JSON 文件
3. 查看：
   - 价格快照（Gold, USD, Yield, VIX）
   - What Happened（最重要的 5 个事件）
   - Why It Matters（最活跃的 3 个因子）
   - What to Watch Next（即将到来的重要事件）
   - 金价与美元走势图
   - **影响因素曲线**（核心功能）

## 核心功能说明

### 1. 影响因素曲线（Factor Influence Curve）

这是系统的标志性功能。它展示：
- **横轴**：时间
- **纵轴**：各因子的归一化影响力（0-1）
- **意义**：哪些因子在哪个时期对金价解释权最强

**示例解读：**
- 如果看到"A1_REAL_YIELD"（实际利率）曲线在上升 → 说明最近利率因素对金价影响增强
- 如果"D1_GEOPOLITICAL"突然飙升 → 说明地缘政治事件成为主导叙事

**这不是预测，而是叙事可视化。**

### 2. 每日简报结构

```
Today in Gold - 2024-01-31

💰 PRICE SNAPSHOT
   Gold: $2043.50 (+0.45%)
   USD Index: 103.25
   10Y Yield: 4.12%

📰 WHAT HAPPENED (Top 3)
   1. Fed Holds Rates Steady...
   2. Middle East Tensions Rise...
   3. ETF Inflows Continue...

🎯 WHY IT MAY MATTER
   • Real Yields
     Influence: 35.2% | Events: 3
   • Geopolitical Conflict
     Influence: 28.7% | Events: 2

👀 WHAT TO WATCH NEXT
   • US CPI (Monthly, ~13th)
   • FOMC Meeting (~8 times per year)
```

### 3. 6 大因子域

系统将所有事件映射到这些因子：

**A) Monetary & Rates**（货币政策与利率）
- A1_REAL_YIELD: 实际利率
- A2_POLICY_PATH: 政策路径预期
- A3_QE_QT: QE/QT 与金融稳定

**B) Inflation & Growth**（通胀与增长）
- B1_INFLATION: 通胀水平与意外
- B2_RECESSION_RISK: 衰退风险

**C) FX & Liquidity**（美元与流动性）
- C1_USD_STRENGTH: 美元强弱
- C2_LIQUIDITY: 全球流动性

**D) Risk & Geopolitics**（风险与地缘）
- D1_GEOPOLITICAL: 地缘冲突
- D2_SANCTIONS: 制裁与储备多元化
- D3_POLITICAL_RISK: 政治风险

**E) Physical Market**（实物市场）
- E1_CENTRAL_BANK: 央行购金
- E2_ETF_FLOWS: ETF 申赎
- E3_JEWELRY: 珠宝需求
- E5_SUPPLY: 供给冲击

**F) Market Microstructure**（市场微观）
- F1_POSITIONING: 期货持仓
- F2_TERM_STRUCTURE: 期限结构

## 成本控制

### Gemini API 使用

- **免费额度**：每天 60 次请求
- **本系统用量**：每次运行约 30-50 次请求（处理 30-50 条新闻）
- **建议**：
  - 每天运行 1 次完整分析
  - 或调整 `max_news` 参数减少处理量

```python
# 在 gold_analyzer.py 中调整
results = analyzer.run_full_analysis(
    days_back=30,    # 回溯天数
    max_news=20      # 减少到 20 条以降低 API 调用
)
```

## 故障排除

### 问题 1：No news fetched

**原因**：RSS feeds 可能临时不可用
**解决**：
- 检查网络连接
- 等待几分钟重试
- 或提供 NewsAPI key

### 问题 2：Gemini API error

**原因**：API key 无效或额度用完
**解决**：
- 检查 `.env` 文件中的 key 是否正确
- 访问 https://makersuite.google.com/ 查看配额
- 减少 `max_news` 参数

### 问题 3：Empty chart

**原因**：数据未正确加载
**解决**：
- 确保已运行 `python gold_analyzer.py`
- 检查 `analysis_output/` 目录是否有 JSON 文件
- 在 dashboard 中上传正确的文件

## 下一步优化

这是 MVP 版本。可以扩展的方向：

1. **数据层**
   - 接入付费数据源（Bloomberg, Refinitiv）
   - 添加 ETF 持仓实时追踪
   - 接入经济日历 API

2. **理解层**
   - Fine-tune 模型提高抽取准确性
   - 添加情感分析
   - 实现多语言新闻支持

3. **对齐层**
   - 更复杂的因果推断模型
   - 机器学习预测（谨慎！）
   - 事件影响窗口优化

4. **输出层**
   - 自动生成报告（PDF/PPT）
   - 邮件/Slack 推送
   - 移动端 App

5. **存储**
   - 从 JSON 迁移到 SQLite/PostgreSQL
   - 添加历史数据管理
   - 实现增量更新

## 项目结构

```
gold-price-explainer/
├── README.md                    # 项目说明
├── QUICKSTART.md               # 本文件
├── requirements.txt            # Python 依赖
├── .env.example                # 环境变量模板
├── factor_config.json          # 因子字典（核心）
├── gold_analyzer.py            # 主程序
├── data_fetcher.py             # 数据获取
├── news_fetcher.py             # 新闻获取
├── event_extractor.py          # 事件抽取（Gemini）
├── factor_engine.py            # 因子分析
├── dashboard.html              # 可视化界面
├── data_cache/                 # 市场数据缓存
├── news_cache/                 # 新闻缓存
├── events_output/              # 事件输出
└── analysis_output/            # 分析结果
```

## 联系与反馈

这是一个开源项目模板。欢迎：
- 提交 Issue 报告 bug
- 提交 PR 贡献代码
- Fork 项目进行自定义

**重要提醒**：
⚠️ 本系统是**认知工具**，不是交易信号
⚠️ 所有分析基于历史模式，不构成投资建议
⚠️ 请结合专业金融建议使用

祝使用愉快！🚀
