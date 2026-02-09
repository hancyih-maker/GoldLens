# Gold Price Explainer - 项目架构与实现总结

## 📋 项目概述

这是一个完整的、基于 AI 的黄金价格解释器系统，实现了你规划文档中的所有核心功能。

## 🎯 核心特点

### 1. 完整的分层架构

**数据层 (L0)**
- ✅ 市场时间序列：金价、美元指数、10年期收益率、VIX
- ✅ 新闻流：RSS feeds 自动抓取（免费）
- ✅ 事件日历：预定义重要事件（可扩展）

**理解层 (L1-L2)**
- ✅ 结构化事件抽取（使用 Gemini API）
- ✅ 6 大因子域 × 细分因子映射
- ✅ 影响强度评估（启发式评分）

**对齐层 (L3)**
- ✅ 时间窗口分析
- ✅ 价格-事件共现模式

**输出层 (L4)**
- ✅ 每日 Market Brief（结构化简报）
- ✅ 影响因素曲线可视化（标志性功能）
- ✅ 观察清单

### 2. 6 大因子域实现

完整实现了因子字典（`factor_config.json`）：

```
A) Monetary & Rates（货币政策与利率）
   - A1_REAL_YIELD: 实际利率
   - A2_POLICY_PATH: 政策路径预期
   - A3_QE_QT: QE/QT 与金融稳定

B) Inflation & Growth（通胀与增长）
   - B1_INFLATION: 通胀水平与意外
   - B2_RECESSION_RISK: 衰退风险

C) FX & Liquidity（美元与流动性）
   - C1_USD_STRENGTH: 美元强弱
   - C2_LIQUIDITY: 全球流动性

D) Risk & Geopolitics（风险与地缘）
   - D1_GEOPOLITICAL: 地缘冲突
   - D2_SANCTIONS: 制裁与储备多元化
   - D3_POLITICAL_RISK: 政治风险

E) Physical Market（实物市场）
   - E1_CENTRAL_BANK: 央行购金
   - E2_ETF_FLOWS: ETF 申赎
   - E3_JEWELRY: 珠宝需求
   - E5_SUPPLY: 供给冲击

F) Market Microstructure（市场微观）
   - F1_POSITIONING: 期货持仓
   - F2_TERM_STRUCTURE: 期限结构
```

每个因子都包含：
- 机制说明
- 代理变量
- 相关事件类型
- 典型滞后期
- 典型方向

### 3. 标志性功能：影响因素曲线

**技术实现**：
1. 按日聚合因子分数
2. 滚动窗口（7天）累计强度
3. 每日归一化（所有因子和为 1）
4. 时间序列可视化

**用户价值**：
- 直观看到哪些因子在哪个时期对金价解释权最强
- 这是叙事可视化，不是预测
- 区别于普通新闻产品的核心竞争力

## 📁 文件结构

### 核心模块

| 文件 | 功能 | 行数 |
|------|------|------|
| `gold_analyzer.py` | 主程序，整合所有模块 | ~380 |
| `data_fetcher.py` | 市场数据获取（yfinance） | ~250 |
| `news_fetcher.py` | 新闻抓取（RSS feeds） | ~280 |
| `event_extractor.py` | 事件抽取（Gemini API） | ~270 |
| `factor_engine.py` | 因子分析引擎 | ~320 |
| `factor_config.json` | 因子字典（核心知识库） | ~300 |
| `dashboard.html` | 交互式可视化界面 | ~650 |

### 配置与文档

| 文件 | 说明 |
|------|------|
| `README.md` | 项目说明 |
| `QUICKSTART.md` | 快速开始指南（详细） |
| `requirements.txt` | Python 依赖 |
| `env.example.txt` | 环境变量模板 |

## 🔧 技术栈

### 后端
- **Python 3.8+**
- **AI/ML**: `google-generativeai` (Gemini API)
- **数据**: `yfinance`, `pandas`, `numpy`
- **新闻**: `feedparser`, `requests`

### 前端
- **纯 HTML/CSS/JavaScript**（无构建工具）
- **Chart.js** 用于图表
- 响应式设计

### 数据源（全部免费）
- 市场数据：Yahoo Finance (yfinance)
- 新闻：RSS feeds（Fed, ECB, Reuters, Kitco, IMF 等）
- AI 分析：Gemini API（免费额度每天 60 次）

## 🚀 使用流程

### 1. 安装依赖
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. 配置 API
```bash
# 重命名 env.example.txt 为 .env
# 填入 Gemini API key
GEMINI_API_KEY=your_key_here
```

### 3. 运行分析
```bash
python gold_analyzer.py
```

输出：
- `data_cache/` - 市场数据缓存
- `news_cache/` - 新闻缓存
- `events_output/` - 结构化事件
- `analysis_output/` - 完整分析结果（JSON）

### 4. 查看可视化
```bash
python -m http.server 8000
# 访问 http://localhost:8000/dashboard.html
# 上传 analysis_output/*.json 文件
```

## 💡 核心算法

### 事件影响力评分

```python
event_strength = 
    事件类型重要性 × 
    最强因子强度 × 
    平均置信度 × 
    市场波动环境
```

### 因子影响力曲线

```python
1. 按日聚合：Σ(事件影响 × 因子强度)
2. 滚动窗口：rolling_sum(7天)
3. 归一化：factor_influence / Σ(所有因子)
```

### Gemini 提示词工程

使用严格的 JSON schema 约束：
- 事件类型（8 种）
- 因子标签（代码、极性、强度、置信度）
- 机制路径（因果链）
- 时间范围（intraday 到 6M）

## 📊 示例输出

### 每日简报结构

```json
{
  "title": "Today in Gold",
  "date": "2024-01-31",
  "price_snapshot": {
    "gold_price": 2043.50,
    "change_pct": 0.45,
    "dxy": 103.25,
    "yield": 4.12
  },
  "what_happened": [
    {
      "headline": "Fed Holds Rates Steady...",
      "event_type": "CENTRAL_BANK_DECISION",
      "impact_score": 0.756,
      "factors": ["A1_REAL_YIELD", "A2_POLICY_PATH"]
    }
  ],
  "why_matters": [
    {
      "factor_name": "Real Yields",
      "influence_score": 0.352,
      "event_count": 3
    }
  ],
  "watch_next": [...]
}
```

## 🎨 可视化界面特点

### Dashboard 组件

1. **价格快照卡片**
   - 金价 + 涨跌幅
   - 美元指数、利率、VIX

2. **What Happened 卡片**
   - Top 5 事件
   - 影响力评分
   - 关联因子

3. **Why It Matters 卡片**
   - Top 3 活跃因子
   - 影响力百分比条
   - 相关事件样本

4. **What to Watch 卡片**
   - 即将到来的重要事件
   - 时间表和影响等级

5. **金价走势图**
   - 双轴：金价 + 美元指数
   - 交互式悬停

6. **影响因素曲线**（核心）
   - 多条时间序列
   - 堆叠面积图
   - 归一化展示

### 设计特点

- 💎 **Golden Theme**: 黄金主题色
- 📱 **响应式**: 自适应不同屏幕
- 🎯 **交互式**: Chart.js 图表
- 📊 **数据驱动**: JSON 文件加载

## ⚙️ 配置与扩展

### 调整分析参数

在 `gold_analyzer.py` 中：

```python
results = analyzer.run_full_analysis(
    days_back=30,    # 回溯天数（7-90）
    max_news=50      # 最多处理新闻数（控制成本）
)
```

### 自定义因子

编辑 `factor_config.json`：

```json
{
  "factor_domains": {
    "G_ENVIRONMENT": {
      "name": "Environment & Climate",
      "factors": {
        "G1_CLIMATE_SHOCK": {
          "name": "Climate Impact on Mining",
          "mechanism": "...",
          ...
        }
      }
    }
  }
}
```

### 添加新闻源

在 `news_fetcher.py` 中：

```python
RSS_FEEDS = [
    "https://your-custom-feed.com/rss",
    ...
]
```

## 🔐 成本控制

### Gemini API 用量

- **免费额度**: 60 次/天
- **本系统用量**: 30-50 次/运行
- **建议频率**: 每天 1 次

### 降低成本

```python
# 方法 1: 减少新闻处理量
max_news=20  # 从 50 降到 20

# 方法 2: 增加运行间隔
# 不是每小时运行，改为每天运行

# 方法 3: 本地缓存
# 系统已自动缓存新闻和事件
```

## ⚠️ 重要声明

### 这是认知工具，不是交易信号

- ✅ 用于理解市场叙事
- ✅ 学习因子驱动分析
- ✅ 研究历史模式
- ❌ 不用于实盘交易
- ❌ 不构成投资建议
- ❌ 不保证预测准确性

### MVP 范围

当前实现聚焦于：
- 基础数据源（免费）
- 核心因子框架（6 大域）
- 基本可视化
- 本地文件存储

**未包含**（可扩展）：
- 付费数据源
- 实时推送
- 数据库存储
- 机器学习预测
- 移动端 App

## 🔮 未来扩展方向

### 短期（1-2 周）
1. 添加更多 RSS 源
2. 优化 Gemini 提示词
3. 改进可视化交互
4. 添加导出功能（PDF/CSV）

### 中期（1-2 月）
1. 接入经济日历 API
2. 实现 ETF 持仓追踪
3. 添加历史回测功能
4. SQLite 数据库存储

### 长期（3-6 月）
1. 机器学习因子权重
2. 多资产支持（银、原油）
3. 移动端界面
4. 实时推送系统

## 🛠️ 故障排除

### 常见问题

**Q: 没有抓取到新闻？**
A: 检查网络连接，RSS 源可能临时不可用

**Q: Gemini API 报错？**
A: 检查 API key 是否正确，配额是否用完

**Q: 图表不显示？**
A: 确保已上传正确的 JSON 文件

**Q: 价格数据为空？**
A: yfinance 可能被限流，稍后重试

## 📚 参考资料

### API 文档
- Gemini API: https://ai.google.dev/docs
- yfinance: https://pypi.org/project/yfinance/
- Chart.js: https://www.chartjs.org/

### 金融知识
- World Gold Council: https://www.gold.org/
- Fed: https://www.federalreserve.gov/
- IMF: https://www.imf.org/

## 🙏 致谢

本系统基于：
- Google Gemini AI
- Yahoo Finance 数据
- 开源社区工具

---

**版本**: 1.0 MVP
**日期**: 2024-02-09
**License**: MIT

祝使用愉快！如有问题欢迎反馈。🚀
