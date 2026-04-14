"""pages/market.py — Market impact with export button"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from frontend._data.api_client import get_stock_series, _client, _USE_REAL
from frontend._components.charts import stock_line_chart, category_impact_bar
from frontend.config import INDEX_OPTIONS

# Hardcoded fallback only — real data loaded below
_CAT_IMPACT_FALLBACK = pd.DataFrame({
    "category":   ["Threatening intl.", "Attacking opposition", "Other",
                   "Praising/endorsing", "Self-promotion", "Enacting non-agg.", "De-escalating"],
    "avg_impact": [-0.28, -0.09, -0.01, 0.04, 0.06, 0.09, 0.11],
})

def _get_category_impact() -> pd.DataFrame:
    """Load real category impact from backend, fallback to hardcoded."""
    if _USE_REAL:
        try:
            end   = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            df = _client.get_category_market_impact(start=start, end=end)
            if not df.empty and "sp500_5min_pct" in df.columns:
                return df[["category", "sp500_5min_pct"]].rename(
                    columns={"sp500_5min_pct": "avg_impact"}
                ).sort_values("avg_impact")
        except Exception as e:
            print(f"_get_category_impact error: {e}")
    return _CAT_IMPACT_FALLBACK


def render(T: dict):
    c1, c2 = st.columns([2, 1])
    with c1:
        index_key = st.selectbox(
            T["select_index"],
            options=list(INDEX_OPTIONS.keys()),
            format_func=lambda x: INDEX_OPTIONS[x],
        )
    with c2:
        days = st.slider(T["days_shown"], 7, 60, 30)

    df = get_stock_series(index_key, days)

    # Label the y-axis correctly — pct change for sp500/qqq/dia, price for others
    chart_title = INDEX_OPTIONS[index_key]
    if index_key in ("sp500", "qqq", "dia"):
        st.caption(f"Showing **5-min % change** after each post · {chart_title} · market hours only")
    else:
        st.caption(f"Showing **daily close price** · {chart_title}")

    if df.empty:
        st.warning("📭 No stock data available for this period.")
        return
    st.plotly_chart(stock_line_chart(df, chart_title), use_container_width=True)
    st.caption("⭐ Red stars = posts with large market move (>0.3%)")

    st.divider()
    st.subheader("Avg S&P 500 move by post category (5 min after)")

    cat_df = _get_category_impact()
    st.plotly_chart(category_impact_bar(cat_df), use_container_width=True)
    st.caption(
        "📝 **Interpretation:** Threatening international posts show strongest "
        "negative correlation. Policy posts lean positive. Correlation ≠ causation."
    )

    # ── Export button ─────────────────────────────────────────────────────────
    st.divider()
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        csv_stock = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Export stock data (CSV)",
            data=csv_stock,
            file_name=f"trumpsignal_{index_key}_{days}days.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e2:
        csv_cat = cat_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Export category impact (CSV)",
            data=csv_cat,
            file_name="trumpsignal_category_impact.csv",
            mime="text/csv",
            use_container_width=True,
        )