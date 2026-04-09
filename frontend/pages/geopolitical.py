"""pages/geopolitical.py — Geopolitical (GDELT) tab"""
import streamlit as st
from frontend.data.api_client import get_gdelt_summary, get_gdelt_timeseries
from frontend.components.charts import gdelt_tone_bar, gdelt_breakdown_bar

def render(T: dict):
    st.caption("GDELT global event database · updates weekly")

    gdelt = get_gdelt_summary()
    gt_df = get_gdelt_timeseries(8)

    c1, c2, c3 = st.columns(3)
    c1.metric("Military events",  f"{gdelt['military_events']:,}",
              delta="+34% vs avg", delta_color="inverse")
    c2.metric("Verbal conflict",  f"{gdelt['verbal_conflict']:,}",
              delta="+18% vs avg", delta_color="inverse")
    c3.metric("Avg global tone",  f"{gdelt['avg_tone']:.2f}",
              help="Negative = more conflict globally")

    st.divider()
    st.subheader("Global tone over time")
    st.plotly_chart(gdelt_tone_bar(gt_df), use_container_width=True)

    st.subheader(f"Signal breakdown · {gdelt['week_of']}")
    st.plotly_chart(gdelt_breakdown_bar(gdelt), use_container_width=True)

    st.info(f"**{T['interp']}:** {gdelt['interpretation']}")
