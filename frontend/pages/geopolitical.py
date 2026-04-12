"""pages/geopolitical.py — Geopolitical signals tab"""
import streamlit as st
from frontend.data.api_client import get_gdelt_summary, get_gdelt_timeseries
from frontend.components.charts import gdelt_tone_bar


def render(T: dict):
    st.subheader("Geopolitical Signals (GDELT)")

    summary = get_gdelt_summary()
    df_trend = get_gdelt_timeseries(weeks=8)

    if not summary or df_trend.empty:
        st.warning("GDELT data is not yet available. Please check back later.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", f"{summary.get('total_events', 0):,}")
    col2.metric("Avg Tone", f"{summary.get('avg_tone', 0):.2f}")
    col3.metric("Goldstein Avg", f"{summary.get('goldstein_avg', 0):.2f}")

    if "interpretation" in summary:
        st.info(summary["interpretation"])

    # Use existing chart function from charts.py
    st.plotly_chart(gdelt_tone_bar(df_trend), use_container_width=True)
    st.dataframe(df_trend)