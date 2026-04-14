"""pages/geopolitical.py — Geopolitical with month/year selector"""
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from frontend._data.api_client import get_gdelt_timeseries
from frontend._components.charts import gdelt_tone_bar, gdelt_breakdown_bar

def _get_available_dates():
    """Get available months and years from dataset dynamically"""
    try:
        from backend_database.data_api import TrumpDataClient
        c   = TrumpDataClient()
        df  = c.get_gdelt_trend(start="2020-01-01", end="2099-12-31")
        df["day"] = pd.to_datetime(df["day"])
        min_date  = df["day"].min().date()
        max_date  = df["day"].max().date()
        return min_date, max_date
    except:
        return date(2025, 10, 1), date(2026, 4, 7)

def _get_gdelt_for_range(start: date, end: date) -> pd.DataFrame:
    """Get GDELT data for a specific date range"""
    try:
        from backend_database.data_api import TrumpDataClient
        c  = TrumpDataClient()
        df = c.get_gdelt_trend(
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d")
        )
        if df.empty:
            return pd.DataFrame()
        df["day"] = pd.to_datetime(df["day"])
        df["week"] = df["day"].dt.strftime("%d %b")
        df["avg_tone"] = df["gdelt_avg_tone"].round(2)
        df["verbal_conflict"] = df["gdelt_verbal_conflict"].fillna(0).round(0).astype(int)
        return df
    except Exception as e:
        print(f"GDELT range error: {e}")
        return pd.DataFrame()

def _build_summary(df: pd.DataFrame) -> dict:
    """Build summary dict from a DataFrame"""
    if df.empty:
        return {}
    return {
        "week_of":            df["day"].max().strftime("%d %b %Y"),
        "military_events":    int(df["gdelt_military"].fillna(0).sum()),
        "verbal_conflict":    int(df["gdelt_verbal_conflict"].fillna(0).sum()),
        "verbal_cooperation": int(df["gdelt_verbal_cooperation"].fillna(0).sum()),
        "material_conflict":  int(df["gdelt_material_conflict"].fillna(0).sum()),
        "diplomatic":         0,
        "goldstein_avg":      round(float(df["gdelt_goldstein_avg"].fillna(0).mean()), 2),
        "avg_tone":           round(float(df["gdelt_avg_tone"].fillna(0).mean()), 2),
        "total_events":       int(df["gdelt_total_events"].fillna(0).sum()),
        "interpretation": (
            "Global tension elevated — verbal conflict high."
            if df["gdelt_avg_tone"].mean() < -2 else
            "Moderate tension detected." if df["gdelt_avg_tone"].mean() < -1 else
            "Global tone relatively neutral."
        ),
    }

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
        # Build list of available months
        months = []
        d = min_date.replace(day=1)
        while d <= max_date.replace(day=1):
            months.append(d)
            # next month
            if d.month == 12:
                d = d.replace(year=d.year+1, month=1)
            else:
                d = d.replace(month=d.month+1)
        months.reverse()  # latest first

        selected_month = st.selectbox(
            "Select month",
            options=months,
            format_func=lambda d: d.strftime("%B %Y"),
        )
        start = selected_month
        # last day of month
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

    if df.empty:
        st.warning(f"📭 No GDELT data available for this period.")
        return

    gdelt   = _build_summary(df)
    plot_df = df[["week", "avg_tone", "verbal_conflict"]].reset_index(drop=True)

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Military events",    f"{gdelt['military_events']:,}")
    c2.metric("Verbal conflict",    f"{gdelt['verbal_conflict']:,}")
    c3.metric("Verbal cooperation", f"{gdelt['verbal_cooperation']:,}")
    c4.metric("Avg global tone",    f"{gdelt['avg_tone']:.2f}",
              help="Negative = more conflict globally")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    st.subheader(f"Global tone · {period}")
    st.plotly_chart(gdelt_tone_bar(plot_df), use_container_width=True)

    st.subheader(f"Signal breakdown · {gdelt['week_of']}")
    st.plotly_chart(gdelt_breakdown_bar(gdelt), use_container_width=True)

    st.info(f"**Interpretation:** {gdelt['interpretation']}")

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
