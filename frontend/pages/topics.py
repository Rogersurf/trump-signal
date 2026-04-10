"""pages/topics.py — Topic breakdown with date context"""
import streamlit as st
from datetime import date, timedelta
from frontend.data.api_client import get_category_summary

def render(T: dict):
    today = date.today()

    # Period selector with date context
    col1, col2 = st.columns([2, 3])
    with col1:
        period = st.radio(T["period"],
                          [T["week"], T["month"], T["year"]],
                          horizontal=True)

    period_key = {
        "Week": "week", "Month": "month", "Year": "year",
        "สัปดาห์": "week", "เดือน": "month", "ปี": "year",
        "周": "week", "月": "month", "年": "year",
    }.get(period, "month")

    # Show what date range this covers
    if period_key == "week":
        start = today - timedelta(days=7)
        label = f"{start.strftime('%d %b')} – {today.strftime('%d %b %Y')}"
    elif period_key == "month":
        start = today - timedelta(days=30)
        label = f"{start.strftime('%d %b')} – {today.strftime('%d %b %Y')}"
    else:
        start = today - timedelta(days=365)
        label = f"{start.strftime('%d %b %Y')} – {today.strftime('%d %b %Y')}"

    with col2:
        st.caption(f"Showing: {label}")

    df = get_category_summary(period_key)

    if df.empty:
        st.info("No data available"); return

    # Pie chart
    from frontend.components.charts import pie_chart
    import plotly.express as px
    from frontend.config import CATEGORY_COLORS

    fig = px.pie(
        df, names="category", values="count",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        hole=0.42,
    )
    fig.update_traces(textinfo="label+percent", pull=[0.03] * len(df))
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(
        df.sort_values("count", ascending=False)
          .rename(columns={"category": T["category"], "count": "Posts"}),
        use_container_width=True,
        hide_index=True,
    )
