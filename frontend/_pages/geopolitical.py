"""pages/geopolitical.py — Geopolitical with export button"""
import streamlit as st
import pandas as pd
from frontend._data.api_client import get_gdelt_summary, get_gdelt_timeseries
from frontend._components.charts import gdelt_tone_bar, gdelt_breakdown_bar

def render(T: dict):
    from datetime import date, timedelta
    today     = date(2026, 4, 14)  # dataset max
    month_start = today.replace(day=1)
    st.caption(
        f"GDELT global event database · updates weekly · "
        f"Showing from {month_start.strftime('%d %b %Y')} to {today.strftime('%d %b %Y')}"
    )

    gdelt = get_gdelt_summary()
    if not gdelt:
        st.warning("📭 No GDELT data available for this period.")
        return
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

    # ── Export button ─────────────────────────────────────────────────────────
    st.divider()
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        csv_ts = gt_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Export GDELT timeseries (CSV)",
            data=csv_ts,
            file_name="trumpsignal_gdelt_timeseries.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e2:
        summary_df = pd.DataFrame([{
            "week_of":            gdelt["week_of"],
            "military_events":    gdelt["military_events"],
            "verbal_conflict":    gdelt["verbal_conflict"],
            "verbal_cooperation": gdelt["verbal_cooperation"],
            "material_conflict":  gdelt["material_conflict"],
            "diplomatic":         gdelt["diplomatic"],
            "goldstein_avg":      gdelt["goldstein_avg"],
            "avg_tone":           gdelt["avg_tone"],
            "total_events":       gdelt["total_events"],
        }])
        csv_summary = summary_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Export weekly summary (CSV)",
            data=csv_summary,
            file_name="trumpsignal_gdelt_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )
