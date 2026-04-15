"""pages/topics.py — Topic breakdown with custom date range"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from frontend._data.api_client import get_category_summary
from frontend.config import CATEGORY_COLORS

def render(T: dict):
    today = date.today()

    st.caption("Topic classification is based on the dataset — no model training required.")

    # ── Date range picker ─────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input(
            "From",
            key="topics_start",
            value=date(2022, 1, 1),
            min_value=date(2022, 1, 1),
            max_value=today,
            format="DD/MM/YYYY",
        )
    with col2:
        end = st.date_input(
            "To",
            key="topics_end",
            value=today,
            min_value=date(2022, 1, 1),
            max_value=today,
            format="DD/MM/YYYY",
        )

    if start > end:
        st.error("Start date must be before end date.")
        return

    # ── Get data ──────────────────────────────────────────────────────────────
    period_days = (end - start).days
    if period_days <= 7:
        period = "week"
    elif period_days <= 30:
        period = "month"
    else:
        period = "year"

    df = get_category_summary(period, date_from=str(start), date_to=str(end))

    if df.empty:
        st.warning(f"📭 No topic data available between {start.strftime('%d %b %Y')} and {end.strftime('%d %b %Y')}.")
        return

    df = df[df["count"] > 0].reset_index(drop=True)

    # ── Metrics ───────────────────────────────────────────────────────────────
    total   = df["count"].sum()
    top_cat = df.loc[df["count"].idxmax(), "category"]
    top_pct = round(df["count"].max() / total * 100, 1) if total > 0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Total posts",    f"{total:,.0f}")
    m2.metric("Top category",   top_cat)
    m3.metric("Top category %", f"{top_pct}%")

    st.caption(f"Showing: {start.strftime('%d %b %Y')} – {end.strftime('%d %b %Y')} · {(end-start).days} days")

    st.divider()

    # ── Pie chart ─────────────────────────────────────────────────────────────
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

    # ── Table ─────────────────────────────────────────────────────────────────
    df_display = df.copy()
    df_display["% of total"] = (df_display["count"] / total * 100).round(1).astype(str) + "%"
    st.dataframe(
        df_display.sort_values("count", ascending=False)
                  .rename(columns={"category": "Category", "count": "Posts"}),
        use_container_width=True,
        hide_index=True,
    )

    # ── Export ────────────────────────────────────────────────────────────────
    st.divider()
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.download_button(
            label="⬇️ Export topic breakdown (CSV)",
            data=df_display.to_csv(index=False),
            file_name=f"trumpsignal_topics_{start}_{end}.csv",
            mime="text/csv",
            use_container_width=True,
        )
