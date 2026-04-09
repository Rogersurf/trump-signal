"""pages/topics.py — Topic breakdown pie chart tab"""
import streamlit as st
from frontend.data.api_client import get_category_summary
from frontend.components.charts import pie_chart

def render(T: dict):
    period = st.radio(T["period"],
                      [T["week"], T["month"], T["year"]],
                      horizontal=True)
    period_key = {"Week": "week", "Month": "month", "Year": "year",
                  "สัปดาห์": "week", "เดือน": "month", "ปี": "year",
                  "周": "week", "月": "month", "年": "year"}.get(period, "month")

    df = get_category_summary(period_key)
    st.plotly_chart(pie_chart(df), use_container_width=True)

    st.dataframe(
        df.sort_values("count", ascending=False)
          .rename(columns={"category": T["category"], "count": "Posts"}),
        use_container_width=True, hide_index=True,
    )
