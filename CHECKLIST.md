# 📦 Gold Price Explainer — Project File Inventory

## ✅ Core File List

### 🐍 Python Modules (7)

1. **gold_analyzer.py** (11 KB)

   * Main entry point
   * Orchestrates all modules
   * Generates the daily market brief
   * Run: `python gold_analyzer.py`

2. **data_fetcher.py** (8.0 KB)

   * Market data ingestion
   * Supports: gold, USD, yields, VIX
   * Data source: Yahoo Finance (free)
   * Test: `python data_fetcher.py`

3. **news_fetcher.py** (9.1 KB)

   * News ingestion
   * RSS feeds (7 sources)
   * Optional: NewsAPI integration
   * Test: `python news_fetcher.py`

4. **event_extractor.py** (8.4 KB)

   * Structured event extraction
   * Powered by Gemini API
   * JSON schema constraints
   * Test: `python event_extractor.py`

5. **factor_engine.py** (11 KB)

   * Factor analytics engine
   * Scoring, aggregation, alignment
   * Computes impact curves
   * Test: `python factor_engine.py`

6. **requirements.txt** (356 B)

   * Python dependency list
   * All free libraries
   * Install: `pip install -r requirements.txt --break-system-packages`

### 📊 Config Files (2)

7. **factor_config.json** (8.6 KB)

   * **Core knowledge base**
   * Defines 6 factor domains
   * Event type mappings
   * Mechanism descriptions
   * ⚠️ Important: fully customisable and extensible

8. **env.example.txt** (580 B)

   * Environment variable template
   * Rename to `.env`
   * Add Gemini API key
   * Optional: NewsAPI, Alpha Vantage keys

### 🎨 Frontend UI (1)

9. **dashboard.html** (20 KB)

   * Interactive visual dashboard
   * Fully standalone (no build step)
   * Chart.js charts
   * Usage: `python -m http.server 8000`

### 📚 Documentation (3)

10. **README.md** (2.9 KB)

    * Project overview
    * Feature list
    * System architecture diagram

11. **QUICKSTART.md** (7.4 KB)

    * Detailed setup guide
    * Installation steps
    * Troubleshooting
    * Cost control

12. **PROJECT_SUMMARY.md** (new)

    * Architecture summary
    * Technical details
    * Extension roadmap

---

## 🚀 Quick Start Checklist

### [ ] Step 1: Environment setup

* [ ] Install Python 3.8+
* [ ] Download all project files
* [ ] Install dependencies: `pip install -r requirements.txt --break-system-packages`
* [ ] Verify install: `python -c "import google.generativeai; print('OK')"`

### [ ] Step 2: Configure API

* [ ] Get a Gemini API key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* [ ] Copy `env.example.txt` to `.env`
* [ ] Add your key: `GEMINI_API_KEY=your_key_here`
* [ ] Verify:

  * [ ] `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10])"`

### [ ] Step 3: Test modules

* [ ] Test market data: `python data_fetcher.py`

  * Expected: ✓ Fetched XX days of gold price data

* [ ] Test news ingestion: `python news_fetcher.py`

  * Expected: ✓ Total fetched: XX relevant articles

* [ ] Test event extraction: `python event_extractor.py`

  * Expected: ✓ Event type: CENTRAL_BANK_DECISION

### [ ] Step 4: Run full analysis

* [ ] Run: `python gold_analyzer.py`
* [ ] Wait for completion (~2–5 minutes depending on news volume)
* [ ] Check output folders:

  * [ ] `data_cache/` - market data JSON exists
  * [ ] `news_cache/` - news JSON exists
  * [ ] `events_output/` - event JSON exists
  * [ ] `analysis_output/` - analysis JSON exists

### [ ] Step 5: View dashboard

* [ ] Start web server: `python -m http.server 8000`
* [ ] Open: [http://localhost:8000/dashboard.html](http://localhost:8000/dashboard.html)
* [ ] Upload the latest JSON file from `analysis_output/`
* [ ] Verify all sections render:

  * [ ] Price Snapshot
  * [ ] What Happened
  * [ ] Why It Matters
  * [ ] What to Watch
  * [ ] Gold trend chart
  * [ ] Impact Factor Curves

---

## 📂 Post-run Directory Structure

```
gold-price-explainer/
├── README.md
├── QUICKSTART.md
├── PROJECT_SUMMARY.md
├── requirements.txt
├── .env                          # created by you (from env.example.txt)
├── factor_config.json
├── gold_analyzer.py
├── data_fetcher.py
├── news_fetcher.py
├── event_extractor.py
├── factor_engine.py
├── dashboard.html
│
├── data_cache/                   # auto-created
│   └── market_data_20240209.json
│
├── news_cache/                   # auto-created
│   └── news_20240209_1430.json
│
├── events_output/                # auto-created
│   └── events_20240209_1435.json
│
└── analysis_output/              # auto-created
    └── analysis_20240209_1440.json
```

---

## 🎯 Core Functionality Validation

### ✓ Data layer validation

```bash
# Run data fetch test
python data_fetcher.py

# Expected:
# ✓ Fetched 30 days of gold price data
# ✓ Fetched 30 days of USD index data
# ✓ Fetched 30 days of yield data
# ✓ Fetched 30 days of VIX data
# ✓ Aligned data: 30 rows
```

### ✓ News layer validation

```bash
# Run news ingestion test
python news_fetcher.py

# Expected:
# ✓ Federal Reserve: X articles
# ✓ Reuters: X articles
# ✓ Kitco: X articles
# ✓ Total unique articles: XX
```

### ✓ AI layer validation

```bash
# Run event extraction test (requires GEMINI_API_KEY)
python event_extractor.py

# Expected:
# [1/2] Fed Holds Rates Steady...
#   ✓ Event type: CENTRAL_BANK_DECISION
#   ✓ Factors: A1_REAL_YIELD, A2_POLICY_PATH
```

### ✓ Analytics layer validation

```bash
# Run full analysis
python gold_analyzer.py

# Expected full flow:
# 📊 STEP 1: Fetching Market Data
# 📰 STEP 2: Fetching News
# 🤖 STEP 3: Extracting Events
# 📈 STEP 4: Factor Analysis
# 📝 STEP 5: Generating Daily Brief
# ✓ Full analysis saved to analysis_output/...
```

---

## 🔍 Quick Diagnostics (Common Issues)

### Issue 1: ImportError

**Symptom**: `ModuleNotFoundError: No module named 'xxx'`

**Diagnosis**:

```bash
pip list | grep -i google
pip list | grep -i yfinance
pip list | grep -i pandas
```

**Fix**:

```bash
pip install -r requirements.txt --break-system-packages
```

---

### Issue 2: API key error

**Symptom**: `Error: Invalid API key` or `403 Forbidden`

**Diagnosis**:

```bash
# Check .env exists
ls -la .env

# Check contents
cat .env | grep GEMINI

# Quick key sanity check
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f'Key length: {len(key) if key else 0}')
print(f'Starts with: {key[:10] if key else None}')
"
```

**Fix**:

1. Confirm `.env` exists (not `env.example.txt`)
2. Ensure the key is copied correctly (no extra spaces/newlines)
3. Regenerate a key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

### Issue 3: No news fetched

**Symptom**: `✓ Total fetched: 0 relevant articles`

**Diagnosis**:

```bash
# Test connectivity to a feed
curl -I https://www.federalreserve.gov/feeds/press_all.xml

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**Fix**:

1. Check your connection
2. Try again later (feeds can be temporarily down)
3. If you have a NewsAPI key, add it to `.env`

---

### Issue 4: Gemini quota exceeded

**Symptom**: `Resource exhausted` or `Quota exceeded`

**Diagnosis**:
Check quota at [https://makersuite.google.com/](https://makersuite.google.com/)

**Fix**:

1. Wait for quota reset (typically ~24 hours)
2. Reduce `max_news`:

```python
# In gold_analyzer.py
results = analyzer.run_full_analysis(
    days_back=30,
    max_news=10
)
```

---

### Issue 5: Blank dashboard

**Symptom**: Page loads but shows no data

**Diagnosis**:

1. Open browser console (F12)
2. Confirm you uploaded the correct JSON file
3. Inspect the JSON content

**Fix**:

```bash
# Check outputs exist
ls -lh analysis_output/

# Validate JSON structure
python -c "
import json
with open('analysis_output/analysis_XXXXX.json') as f:
    data = json.load(f)
    print('Keys:', list(data.keys()))
    print('Brief keys:', list(data['daily_brief'].keys()))
"
```

---

## 💰 Cost Estimate

### Gemini API (main cost)

| Scenario                   | Requests | Free quota | Cost |
| -------------------------- | -------: | ---------: | ---- |
| Single run (30 news items) |      ~30 |     60/day | $0   |
| 1 run per day              |      ~30 |          ✓ | $0   |
| 2 runs per day             |      ~60 |          ✓ | $0   |
| 3 runs per day             |      ~90 |    30 over | paid |

**Recommendation**: one full run per day is sufficient.

### Other services (all free)

* Yahoo Finance: free
* RSS feeds: free
* Chart.js: free (CDN)
* Storage: local filesystem

**Total**: free for normal usage ✅

---

## 📊 Performance Notes

### Runtime (typical)

* Data fetch: ~10s
* News fetch: ~15s
* Event extraction (30 items): ~60–90s (API dependent)
* Factor analytics: ~2s
* **Total**: ~2–3 minutes

### Data volume

* Market data: ~30 KB / 30 days
* News cache: ~200 KB / 50 items
* Event output: ~100 KB / 50 items
* Analysis output: ~500 KB (includes all data)

---

## ✨ Next Actions

### Get started (5 minutes)

1. [ ] Install dependencies
2. [ ] Configure API key
3. [ ] Run the first analysis
4. [ ] Open the dashboard

### Go deeper (30 minutes)

1. [ ] Read `QUICKSTART.md`
2. [ ] Inspect `factor_config.json`
3. [ ] Understand the impact curves
4. [ ] Try adjusting parameters

### Customise (1–2 hours)

1. [ ] Add new factors
2. [ ] Add more RSS sources
3. [ ] Improve Gemini prompts
4. [ ] Enhance the dashboard UI

---

## 📞 Getting Help

### Docs

* `README.md` - overview
* `QUICKSTART.md` - setup and usage
* `PROJECT_SUMMARY.md` - architecture

### Online resources

* Gemini API: [https://ai.google.dev/docs](https://ai.google.dev/docs)
* yfinance: [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)
* python-dotenv: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

### Debug tips

1. Test modules individually
2. Inspect cached JSON files
3. Add `print()` statements
4. Validate JSON structure
5. Use the browser console (F12)

---

**Final reminder:**

⚠️ This is an interpretation tool, not a trading signal.
⚠️ MVP version—features can be extended.
⚠️ Watch your API quota to avoid overuse.

Enjoy! 🚀


# 📦 Gold Price Explainer - 项目文件清单

## ✅ 核心文件列表

### 🐍 Python 模块（7 个）

1. **gold_analyzer.py** (11 KB)
   - 主程序入口
   - 整合所有模块
   - 生成每日简报
   - 执行: `python gold_analyzer.py`

2. **data_fetcher.py** (8.0 KB)
   - 市场数据获取
   - 支持：金价、美元、利率、VIX
   - 数据源：Yahoo Finance (免费)
   - 测试: `python data_fetcher.py`

3. **news_fetcher.py** (9.1 KB)
   - 新闻抓取
   - RSS feeds（7 个源）
   - 可选：NewsAPI 集成
   - 测试: `python news_fetcher.py`

4. **event_extractor.py** (8.4 KB)
   - 事件结构化抽取
   - 使用 Gemini API
   - JSON schema 约束
   - 测试: `python event_extractor.py`

5. **factor_engine.py** (11 KB)
   - 因子分析引擎
   - 评分、聚合、对齐
   - 影响曲线计算
   - 测试: `python factor_engine.py`

6. **requirements.txt** (356 B)
   - Python 依赖列表
   - 全部免费库
   - 安装: `pip install -r requirements.txt --break-system-packages`

### 📊 配置文件（2 个）

7. **factor_config.json** (8.6 KB)
   - **核心知识库**
   - 6 大因子域定义
   - 事件类型映射
   - 机制说明
   - ⚠️ 重要：可自定义扩展

8. **env.example.txt** (580 B)
   - 环境变量模板
   - 重命名为 `.env` 使用
   - 填入 Gemini API key
   - 可选：NewsAPI, Alpha Vantage keys

### 🎨 前端界面（1 个）

9. **dashboard.html** (20 KB)
   - 交互式可视化仪表板
   - 完全独立（无需构建）
   - Chart.js 图表
   - 使用: `python -m http.server 8000`

### 📚 文档（3 个）

10. **README.md** (2.9 KB)
    - 项目说明
    - 功能特点
    - 系统架构图

11. **QUICKSTART.md** (7.4 KB)
    - 详细使用指南
    - 安装步骤
    - 故障排除
    - 成本控制

12. **PROJECT_SUMMARY.md** (新建)
    - 架构总结
    - 技术细节
    - 扩展方向

---

## 🚀 快速开始检查清单

### [ ] 第一步：环境准备

- [ ] 安装 Python 3.8+
- [ ] 下载所有项目文件
- [ ] 安装依赖：`pip install -r requirements.txt --break-system-packages`
- [ ] 验证安装：`python -c "import google.generativeai; print('OK')"`

### [ ] 第二步：配置 API

- [ ] 获取 Gemini API key：https://makersuite.google.com/app/apikey
- [ ] 复制 `env.example.txt` 为 `.env`
- [ ] 填入 API key：`GEMINI_API_KEY=your_key_here`
- [ ] 验证：`python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10])"`

### [ ] 第三步：测试模块

- [ ] 测试数据获取：`python data_fetcher.py`
  - 期望输出：✓ Fetched XX days of gold price data
  
- [ ] 测试新闻抓取：`python news_fetcher.py`
  - 期望输出：✓ Total fetched: XX relevant articles
  
- [ ] 测试事件抽取：`python event_extractor.py`
  - 期望输出：✓ Event type: CENTRAL_BANK_DECISION

### [ ] 第四步：运行完整分析

- [ ] 执行主程序：`python gold_analyzer.py`
- [ ] 等待完成（约 2-5 分钟，取决于新闻数量）
- [ ] 检查输出目录：
  - [ ] `data_cache/` - 有市场数据 JSON
  - [ ] `news_cache/` - 有新闻 JSON
  - [ ] `events_output/` - 有事件 JSON
  - [ ] `analysis_output/` - 有分析结果 JSON

### [ ] 第五步：查看可视化

- [ ] 启动 Web 服务器：`python -m http.server 8000`
- [ ] 打开浏览器：http://localhost:8000/dashboard.html
- [ ] 上传分析结果：`analysis_output/` 中最新的 JSON 文件
- [ ] 验证所有卡片正常显示：
  - [ ] Price Snapshot
  - [ ] What Happened
  - [ ] Why It Matters
  - [ ] What to Watch
  - [ ] 金价走势图
  - [ ] 影响因素曲线

---

## 📂 运行后的目录结构

```
gold-price-explainer/
├── README.md
├── QUICKSTART.md
├── PROJECT_SUMMARY.md
├── requirements.txt
├── .env                          # 你创建的（从 env.example.txt）
├── factor_config.json
├── gold_analyzer.py
├── data_fetcher.py
├── news_fetcher.py
├── event_extractor.py
├── factor_engine.py
├── dashboard.html
│
├── data_cache/                   # 自动创建
│   └── market_data_20240209.json
│
├── news_cache/                   # 自动创建
│   └── news_20240209_1430.json
│
├── events_output/                # 自动创建
│   └── events_20240209_1435.json
│
└── analysis_output/              # 自动创建
    └── analysis_20240209_1440.json
```

---

## 🎯 核心功能验证

### ✓ 数据层验证

```bash
# 运行数据获取测试
python data_fetcher.py

# 期望看到：
# ✓ Fetched 30 days of gold price data
# ✓ Fetched 30 days of USD index data
# ✓ Fetched 30 days of yield data
# ✓ Fetched 30 days of VIX data
# ✓ Aligned data: 30 rows
```

### ✓ 新闻层验证

```bash
# 运行新闻抓取测试
python news_fetcher.py

# 期望看到：
# ✓ Federal Reserve: X articles
# ✓ Reuters: X articles
# ✓ Kitco: X articles
# ✓ Total unique articles: XX
```

### ✓ AI 层验证

```bash
# 运行事件抽取测试（需要设置 GEMINI_API_KEY）
python event_extractor.py

# 期望看到：
# [1/2] Fed Holds Rates Steady...
#   ✓ Event type: CENTRAL_BANK_DECISION
#   ✓ Factors: A1_REAL_YIELD, A2_POLICY_PATH
```

### ✓ 分析层验证

```bash
# 运行完整分析
python gold_analyzer.py

# 期望看到完整流程：
# 📊 STEP 1: Fetching Market Data
# 📰 STEP 2: Fetching News
# 🤖 STEP 3: Extracting Events
# 📈 STEP 4: Factor Analysis
# 📝 STEP 5: Generating Daily Brief
# ✓ Full analysis saved to analysis_output/...
```

---

## 🔍 常见问题快速诊断

### 问题 1: ImportError

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**诊断**:
```bash
pip list | grep -i google
pip list | grep -i yfinance
pip list | grep -i pandas
```

**解决**:
```bash
pip install -r requirements.txt --break-system-packages
```

---

### 问题 2: API Key 错误

**症状**: `Error: Invalid API key` 或 `403 Forbidden`

**诊断**:
```bash
# 检查 .env 文件存在
ls -la .env

# 检查内容
cat .env | grep GEMINI

# 测试 API key
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f'Key length: {len(key) if key else 0}')
print(f'Starts with: {key[:10] if key else None}')
"
```

**解决**:
1. 确认 `.env` 文件存在（不是 `env.example.txt`）
2. 检查 API key 是否正确复制（无空格、换行）
3. 重新生成 API key：https://makersuite.google.com/app/apikey

---

### 问题 3: 没有新闻数据

**症状**: `✓ Total fetched: 0 relevant articles`

**诊断**:
```bash
# 测试网络连接
curl -I https://www.federalreserve.gov/feeds/press_all.xml

# 检查代理设置
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**解决**:
1. 检查网络连接
2. 尝试不同时间（RSS 源可能临时不可用）
3. 如果有 NewsAPI key，添加到 `.env`

---

### 问题 4: Gemini 配额用完

**症状**: `Resource exhausted` 或 `Quota exceeded`

**诊断**:
访问 https://makersuite.google.com/ 查看配额

**解决**:
1. 等待配额重置（通常 24 小时）
2. 减少 `max_news` 参数：
```python
# 在 gold_analyzer.py 中
results = analyzer.run_full_analysis(
    days_back=30,
    max_news=10  # 减少到 10
)
```

---

### 问题 5: Dashboard 空白

**症状**: 页面加载但无数据

**诊断**:
1. 检查浏览器控制台（F12）
2. 确认上传了正确的 JSON 文件
3. 检查 JSON 文件内容

**解决**:
```bash
# 检查分析输出文件
ls -lh analysis_output/

# 验证 JSON 格式
python -c "
import json
with open('analysis_output/analysis_XXXXX.json') as f:
    data = json.load(f)
    print('Keys:', list(data.keys()))
    print('Brief keys:', list(data['daily_brief'].keys()))
"
```

---

## 💰 成本估算

### Gemini API（核心成本）

| 场景 | 请求次数 | 免费额度 | 成本 |
|------|----------|----------|------|
| 单次运行（30条新闻） | ~30 | 60/天 | $0 |
| 每天 1 次 | ~30 | ✓ | $0 |
| 每天 2 次 | ~60 | ✓ | $0 |
| 每天 3 次 | ~90 | 超额 30 | 需付费 |

**建议**: 每天运行 1 次即可

### 其他服务（全部免费）

- Yahoo Finance: 免费
- RSS Feeds: 免费
- Chart.js: 免费（CDN）
- 存储: 本地文件系统

**总计**: 正常使用完全免费 ✅

---

## 📊 性能指标

### 运行时间（参考）

- 数据获取: ~10 秒
- 新闻抓取: ~15 秒
- 事件抽取（30条）: ~60-90 秒（取决于 API 响应）
- 因子分析: ~2 秒
- **总计**: ~2-3 分钟

### 数据量

- 市场数据: ~30 KB/30 天
- 新闻缓存: ~200 KB/50 条
- 事件输出: ~100 KB/50 条
- 分析结果: ~500 KB（含所有数据）

---

## ✨ 下一步行动

### 立即开始（5 分钟）

1. [ ] 安装依赖
2. [ ] 配置 API key
3. [ ] 运行第一次分析
4. [ ] 查看 Dashboard

### 深入了解（30 分钟）

1. [ ] 阅读 `QUICKSTART.md`
2. [ ] 研究 `factor_config.json`
3. [ ] 理解影响因素曲线
4. [ ] 尝试调整参数

### 自定义扩展（1-2 小时）

1. [ ] 添加新的因子
2. [ ] 接入更多 RSS 源
3. [ ] 优化 Gemini 提示词
4. [ ] 美化 Dashboard

---

## 📞 获取帮助

### 文档

- `README.md` - 项目概述
- `QUICKSTART.md` - 详细指南
- `PROJECT_SUMMARY.md` - 技术架构

### 在线资源

- Gemini API: https://ai.google.dev/docs
- yfinance: https://pypi.org/project/yfinance/
- Python-dotenv: https://pypi.org/project/python-dotenv/

### 调试技巧

1. 单独测试每个模块
2. 查看缓存文件内容
3. 使用 `print()` 调试
4. 检查 JSON 文件格式
5. 浏览器控制台（F12）

---

**最后提醒**：

⚠️ 这是认知工具，不是交易信号
⚠️ MVP 版本，功能可继续扩展
⚠️ 注意 API 配额，避免过度使用

祝使用愉快！🚀
