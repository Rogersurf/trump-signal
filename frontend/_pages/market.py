"""pages/market.py — Market impact with export button"""
import streamlit as st
import pandas as pd
from frontend._data.api_client import get_stock_series
from frontend._components.charts import stock_line_chart, category_impact_bar
from frontend.config import INDEX_OPTIONS

CAT_IMPACT_DATA = pd.DataFrame({
    "category":   ["Threatening intl.", "Attacking opposition", "Other",
                   "Praising/endorsing", "Self-promotion", "Enacting non-agg.", "De-escalating"],
    "avg_impact": [-0.28, -0.09, -0.01, 0.04, 0.06, 0.09, 0.11],
})

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
    st.plotly_chart(stock_line_chart(df, INDEX_OPTIONS[index_key]), use_container_width=True)
    st.caption("⭐ Red stars = days with high-engagement Trump posts")

    st.divider()
    st.subheader("Avg S&P 500 move by post category (5 min after)")
    st.plotly_chart(category_impact_bar(CAT_IMPACT_DATA), use_container_width=True)
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
        csv_cat = CAT_IMPACT_DATA.to_csv(index=False)
        st.download_button(
            label="⬇️ Export category impact (CSV)",
            data=csv_cat,
            file_name="trumpsignal_category_impact.csv",
            mime="text/csv",
            use_container_width=True,
        )
