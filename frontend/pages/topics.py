"""pages/topics.py — Topic breakdown pie chart tab"""
import streamlit as st
from frontend.data.api_client import get_category_summary
from frontend.components.charts import pie_chart

def render(T: dict):
    period = st.selectbox(T["period"], [T["week"], T["month"], T["year"]])
    period_key = {"Week": "week", "Month": "month", "Year": "year"}.get(period, "month")

    df = get_category_summary(period_key)

    if df.empty:
        st.warning("Category data is not yet available. Please check back later.")
    else:
        st.plotly_chart(pie_chart(df), use_container_width=True)
        st.dataframe(df.sort_values("count", ascending=False))
