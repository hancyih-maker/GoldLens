# Gold Price Explainer

An AI-powered gold market analysis system that provides **factor-driven interpretation** and **visual explanations** for gold price movements.

## Key Features

* 📊 **Real-time price tracking**: Gold spot, U.S. Dollar Index (DXY), 10-year real yield
* 📰 **Intelligent news analysis**: Automatically extracts events, classifies them, and attributes them to **six major factor domains**
* 📈 **Impact Factor Curves**: Visualises how each factor’s explanatory weight changes over time
* 📝 **Daily market brief**: A structured “Today in Gold” Market Brief
* 🔍 **Watchlist**: Forward-looking reminders based on the macro event calendar

## System Architecture

```
Data Layer (L0)
  ├─ Market time series: Gold price, DXY, real yields
  ├─ News stream: RSS/API macro news ingestion
  └─ Event calendar: CPI, FOMC, rate decisions, etc.

Understanding Layer (L1–L2)
  ├─ Structured event extraction (Gemini API)
  ├─ Factor mapping: 6 super-domains × sub-factors
  └─ Impact strength estimation

Alignment Layer (L3)
  ├─ Event window analysis (T-1 to T+3)
  └─ Price–event co-occurrence patterns

Output Layer (L4)
  ├─ Daily Market Brief
  ├─ Impact Factor Curve visualisations
  └─ Watchlist
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Configure API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key  # optional
NEWS_API_KEY=your_news_api_key  # optional
```

### 3. Run the system

```bash
# Data collection and analysis
python gold_analyzer.py

# Launch the Web UI
python -m http.server 8000
# Visit http://localhost:8000/dashboard.html
```

## Core Modules

* `gold_analyzer.py` - Main orchestration and analysis engine
* `factor_engine.py` - Factor mapping and scoring engine
* `data_fetcher.py` - Market data ingestion
* `event_extractor.py` - Event extraction (powered by Gemini)
* `factor_config.json` - Factor ontology / dictionary configuration
* `dashboard.html` - Interactive visual dashboard

## Six Factor Domains

1. **A) Monetary & Rates** - Monetary policy and interest rates
2. **B) Inflation & Growth** - Inflation and growth expectations
3. **C) FX & Liquidity** - USD and global liquidity
4. **D) Risk & Geopolitics** - Risk sentiment and geopolitics
5. **E) Physical Market** - Physical supply and demand
6. **F) Market Microstructure** - Market microstructure

## MVP Scope

The current MVP focuses on:

* ✅ Core market data (gold, USD, rates)
* ✅ RSS / free news sources (20–50 items per day)
* ✅ Gemini API–based event extraction
* ✅ Baseline mapping across the six factor domains
* ✅ A simple daily market brief
* ✅ Impact Factor Curve visualisation

## Tech Stack

* **Backend**: Python 3.8+
* **AI**: Google Gemini API
* **Data**: Alpha Vantage, Yahoo Finance, NewsAPI
* **Visualisation**: Chart.js, HTML/CSS/JavaScript
* **Storage**: JSON files (MVP) / extensible to SQLite

## Notes

⚠️ This system is a **research and interpretation tool**, not a trading signal system.
⚠️ All analysis is based on historical patterns and heuristic scoring rules.
⚠️ Please use alongside professional financial advice.

## License

MIT License
