"""pages/geopolitical.py — Geopolitical with month/year selector"""
import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta
from frontend._data.api_client import get_gdelt_timeseries
from frontend._components.charts import gdelt_tone_bar, gdelt_breakdown_bar
from frontend.config import API_URL


def _get_available_dates():
    """Fetch min/max dates from the API."""
    try:
        r = requests.get(f"{API_URL}/data/available_dates", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                dates = [pd.to_datetime(d).date() for d in data if d]
                if dates:
                    return min(dates), max(dates)
    except Exception:
        pass
    return date(2022, 1, 1), date.today()


def _get_gdelt_for_range(start: date, end: date) -> pd.DataFrame:
    """Fetch GDELT trend data from the API."""
    try:
        r = requests.get(
            f"{API_URL}/gdelt/range",
            params={"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                df = pd.DataFrame(data)
                df["day"] = pd.to_datetime(df["day"])
                df["week"] = df["day"].dt.strftime("%d %b")
                df["avg_tone"] = df["gdelt_avg_tone"].round(2)
                df["verbal_conflict"] = df["gdelt_verbal_conflict"].fillna(0).round(0).astype(int)
                return df
    except Exception as e:
        print(f"GDELT range error: {e}")
    return pd.DataFrame()


def _get_gdelt_summary(start: date, end: date) -> dict:
    """Fetch GDELT summary from the API."""
    try:
        r = requests.get(
            f"{API_URL}/gdelt/summary",
            params={"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                if not data:
                    return {}
                # Aggregate all days in the period
                return {
                    "gdelt_military": sum(d.get("gdelt_military", 0) for d in data),
                    "gdelt_verbal_conflict": sum(d.get("gdelt_verbal_conflict", 0) for d in data),
                    "gdelt_material_conflict": sum(d.get("gdelt_material_conflict", 0) for d in data),
                    "gdelt_verbal_cooperation": sum(d.get("gdelt_verbal_cooperation", 0) for d in data),
                    "gdelt_avg_tone": sum(d.get("gdelt_avg_tone", 0) for d in data) / len(data),
                    "week_of": f"{start.strftime('%d %b')} - {end.strftime('%d %b')}",
                    "interpretation": f"Aggregated over {len(data)} days",
                    # Keep the last day's full data for breakdown chart
                    "last_day": data[-1] if data else {}
                }
            return data
    except Exception as e:
        print(f"GDELT summary error: {e}")
    return {}


def render(T: dict):
    st.caption("GDELT global event database · updates weekly · real data from dataset")

    min_date, max_date = _get_available_dates()

    # ── Period selector ───────────────────────────────────────────────────────
    period = st.radio(
        "Period",
        ["This month", "By month", "By year", "All time"],
        horizontal=True,
        key="geo_period",
    )

    # ── Sub-selector based on period ──────────────────────────────────────────
    if period == "This month":
        start = max_date.replace(day=1)
        end   = max_date

    elif period == "By month":
        months = []
        d = min_date.replace(day=1)
        while d <= max_date.replace(day=1):
            months.append(d)
            if d.month == 12:
                d = d.replace(year=d.year+1, month=1)
            else:
                d = d.replace(month=d.month+1)
        months.reverse()

        selected_month = st.selectbox(
            "Select month",
            options=months,
            format_func=lambda d: d.strftime("%B %Y"),
        )
        start = selected_month
        if selected_month.month == 12:
            end = selected_month.replace(year=selected_month.year+1, month=1, day=1) - timedelta(days=1)
        else:
            end = selected_month.replace(month=selected_month.month+1, day=1) - timedelta(days=1)
        end = min(end, max_date)

    elif period == "By year":
        years = list(range(min_date.year, max_date.year + 1))
        years.reverse()
        selected_year = st.selectbox(
            "Select year",
            options=years,
            format_func=lambda y: str(y),
        )
        start = date(selected_year, 1, 1)
        end   = min(date(selected_year, 12, 31), max_date)

    else:  # All time
        start = min_date
        end   = max_date

    st.caption(f"Showing: **{start.strftime('%d %b %Y')}** – **{end.strftime('%d %b %Y')}** · Latest available data: **{max_date.strftime('%d %b %Y')}**")

    # ── Get data ──────────────────────────────────────────────────────────────
    df = _get_gdelt_for_range(start, end)
    gdelt = _get_gdelt_summary(start, end)

    if df.empty or not gdelt:
        st.warning(f"📭 No GDELT data available for this period.")
        return

    # Use daily data for the chart with display_date column
    plot_df = df[["day", "avg_tone", "verbal_conflict"]].copy()
    plot_df["display_date"] = plot_df["day"].dt.strftime("%d %b")

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Military events",    f"{gdelt.get('gdelt_military', 0):,}")
    c2.metric("Verbal conflict",    f"{gdelt.get('gdelt_verbal_conflict', 0):,}")
    c3.metric("Verbal cooperation", f"{gdelt.get('gdelt_verbal_cooperation', 0):,}")
    c4.metric("Material conflict",  f"{gdelt.get('gdelt_material_conflict', 0):,}")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    st.subheader(f"Global tone · {period}")
    st.plotly_chart(gdelt_tone_bar(plot_df), use_container_width=True)

    # Use the last day for the breakdown chart
    breakdown_data = gdelt.get("last_day", gdelt)
    st.subheader(f"Signal breakdown · {breakdown_data.get('day', '')[:10]}")
    st.plotly_chart(gdelt_breakdown_bar(breakdown_data), use_container_width=True)
    st.info(f"**Interpretation:** {gdelt.get('interpretation', '')}")

    # ── Export ────────────────────────────────────────────────────────────────
    st.divider()
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.download_button(
            label="⬇️ Export GDELT timeseries (CSV)",
            data=plot_df.to_csv(index=False),
            file_name=f"trumpsignal_gdelt_{period.replace(' ','_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e2:
        st.download_button(
            label="⬇️ Export summary (CSV)",
            data=pd.DataFrame([gdelt]).to_csv(index=False),
            file_name="trumpsignal_gdelt_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )