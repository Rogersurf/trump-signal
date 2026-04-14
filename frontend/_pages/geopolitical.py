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
            return pd.to_datetime(data["min_date"]).date(), pd.to_datetime(data["max_date"]).date()
    except Exception as e:
        print(f"_get_available_dates error: {e}")
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
            return r.json()
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

    plot_df = df[["week", "avg_tone", "verbal_conflict"]].reset_index(drop=True)

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Military events",    f"{gdelt.get('military_events', 0):,}")
    c2.metric("Verbal conflict",    f"{gdelt.get('verbal_conflict', 0):,}")
    c3.metric("Verbal cooperation", f"{gdelt.get('verbal_cooperation', 0):,}")
    c4.metric("Avg global tone",    f"{gdelt.get('avg_tone', 0):.2f}",
              help="Negative = more conflict globally")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    st.subheader(f"Global tone · {period}")
    st.plotly_chart(gdelt_tone_bar(plot_df), use_container_width=True)

    st.subheader(f"Signal breakdown · {gdelt.get('week_of', '')}")
    st.plotly_chart(gdelt_breakdown_bar(gdelt), use_container_width=True)

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