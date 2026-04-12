"""pages/market.py — Market impact tab"""
import streamlit as st
import pandas as pd
from frontend.data.api_client import get_stock_series
from frontend.components.charts import stock_line_chart, category_impact_bar
from frontend.config import INDEX_OPTIONS

CAT_IMPACT_DATA = pd.DataFrame({
    "category":   ["Threatening intl.", "Attacking opposition", "Other",
                   "Praising/endorsing", "Self-promotion", "Enacting non-agg.", "De-escalating"],
    "avg_impact": [-0.28, -0.09, -0.01, 0.04, 0.06, 0.09, 0.11],
})

def render(T: dict):
    c1, c2 = st.columns([2, 1])
    with c1:
        index_key = st.selectbox(T["select_index"], list(INDEX_OPTIONS.keys()),
                                 format_func=lambda x: INDEX_OPTIONS[x])
    with c2:
        days = st.slider(T["days_shown"], 7, 60, 30)

    df = get_stock_series(index_key, days)

    if df.empty:
        st.warning("Stock data is not yet available. Please check back later.")
    else:
        st.plotly_chart(
            stock_line_chart(df, INDEX_OPTIONS[index_key]),
            use_container_width=True,
        )
        st.caption("⭐ Red stars = days with high-engagement Trump posts")

    st.divider()
    st.subheader("Average S&P 500 move by post category (5 min after post)")
    st.plotly_chart(category_impact_bar(CAT_IMPACT_DATA), use_container_width=True)
    st.caption(
        "📝 **Interpretation:** Threatening international posts show the strongest "
        "negative correlation with S&P 500. Enacting non-aggressive policy posts "
        "lean positive. Note: correlation ≠ causation — other market forces always co-exist."
    )