# Changelog

## v1.0.0 (2026-04-14)

### Frontend
- Daily feed with real Trump posts from dataset
- Live clock and NYSE market status
- Stock selector (12 stocks: S&P500, QQQ, DJT, Gold, Bonds, Oil, Bitcoin, etc.)
- Sentiment filter removed — dataset classification used instead
- ML prediction — next day HIGH/LOW market impact (XGBoost model)
- Topic breakdown with custom date range picker
- Market impact page with period selector (This month/By month/By year/All time)
- Geopolitical page with GDELT data and period selector
- Q&A semantic search with ChromaDB embeddings (all-MiniLM-L6-v2)
- All stock market impact in Q&A results
- Export buttons on Market, Geopolitical, Topics pages
- No mock data — shows "data unavailable" when no data exists
- Dynamic max date from DB — auto-updates when dataset updates

### Data
- 32,429 Trump Truth Social posts (chrissoria/trump-truth-social)
- ChromaDB embeddings for semantic search
- SQLite database (truth_social table)
- GDELT geopolitical signals

### ML
- XGBoost next-day market impact predictor
- Features: post categories, GDELT signals, rolling aggregates
