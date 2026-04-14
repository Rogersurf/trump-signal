"""pages/market.py — Market impact with period selector"""
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from frontend._data.api_client import get_stock_series, _client, _USE_REAL
from frontend._components.charts import stock_line_chart, category_impact_bar
from frontend.config import INDEX_OPTIONS

def _get_available_dates():
    """Get dataset max date dynamically"""
    try:
        df = _client.get_full_data()
        if not df.empty:
            return pd.to_datetime(df["date"]).max().date()
    except:
        pass
    return date(2026, 4, 14)

def _get_date_range(period: str, max_date: date):
    if period == "This month":
        return max_date.replace(day=1), max_date
    elif period == "By month":
        return None, None  # handled separately
    elif period == "By year":
        return None, None  # handled separately
    else:  # All time
        return date(2022, 1, 1), max_date

def _get_category_impact(start: date, end: date) -> pd.DataFrame:
    if _USE_REAL:
        try:
            df = _client.get_category_market_impact(
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d")
            )
            if not df.empty and "sp500_5min_pct" in df.columns:
                return df[["category", "sp500_5min_pct"]].rename(
                    columns={"sp500_5min_pct": "avg_impact"}
                ).sort_values("avg_impact")
        except Exception as e:
            print(f"category impact error: {e}")
    return pd.DataFrame(columns=["category", "avg_impact"])


def render(T: dict):
    max_date = _get_available_dates()

    # ── Controls ──────────────────────────────────────────────────────────────
    c1, c2 = st.columns([2, 3])
    with c1:
        index_key = st.selectbox(
            T["select_index"],
            options=list(INDEX_OPTIONS.keys()),
            format_func=lambda x: INDEX_OPTIONS[x],
        )
    with c2:
        period = st.radio(
            "Period",
            ["This month", "By month", "By year", "All time"],
            horizontal=True,
            key="market_period",
        )

    # ── Sub-selector ──────────────────────────────────────────────────────────
    if period == "By month":
        months = []
        d = date(2022, 1, 1)
        while d <= max_date.replace(day=1):
            months.append(d)
            if d.month == 12:
                d = d.replace(year=d.year+1, month=1)
            else:
                d = d.replace(month=d.month+1)
        months.reverse()
        selected = st.selectbox("Select month", months,
                                format_func=lambda d: d.strftime("%B %Y"),
                                key="market_month")
        start = selected
        if selected.month == 12:
            end = selected.replace(year=selected.year+1, month=1, day=1) - timedelta(days=1)
        else:
            end = selected.replace(month=selected.month+1, day=1) - timedelta(days=1)
        end = min(end, max_date)

    elif period == "By year":
        years = list(range(2022, max_date.year + 1))
        years.reverse()
        selected_year = st.selectbox("Select year", years,
                                     format_func=str, key="market_year")
        start = date(selected_year, 1, 1)
        end   = min(date(selected_year, 12, 31), max_date)

    else:
        start, end = _get_date_range(period, max_date)

    days = (end - start).days
    st.caption(f"Showing: **{start.strftime('%d %b %Y')}** – **{end.strftime('%d %b %Y')}** · {days} days · Latest data: **{max_date.strftime('%d %b %Y')}**")

    # ── Stock chart ───────────────────────────────────────────────────────────
    df = get_stock_series(index_key, days)

    chart_title = INDEX_OPTIONS[index_key]
    if index_key in ("sp500", "qqq", "dia"):
        st.caption(f"Showing **5-min % change** after each post · {chart_title}")
    else:
        st.caption(f"Showing **daily close price** · {chart_title}")

    if df.empty:
        st.warning("📭 No stock data available for this period.")
    else:
        st.plotly_chart(stock_line_chart(df, chart_title), use_container_width=True)
        st.caption("⭐ Red stars = posts with large market move (>0.3%)")

    st.divider()

    # ── Category impact ───────────────────────────────────────────────────────
    st.subheader("Avg S&P 500 move by post category (5 min after)")
    cat_df = _get_category_impact(start, end)
    if cat_df.empty:
        st.warning("📭 No category impact data available for this period.")
    else:
        st.plotly_chart(category_impact_bar(cat_df), use_container_width=True)
        st.caption("📝 Threatening international posts show strongest negative correlation. Correlation ≠ causation.")

    # ── Export ────────────────────────────────────────────────────────────────
    st.divider()
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        if not df.empty:
            st.download_button(
                label="⬇️ Export stock data (CSV)",
                data=df.to_csv(index=False),
                file_name=f"trumpsignal_{index_key}_{period.replace(' ','_')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
    with col_e2:
        if not cat_df.empty:
            st.download_button(
                label="⬇️ Export category impact (CSV)",
                data=cat_df.to_csv(index=False),
                file_name="trumpsignal_category_impact.csv",
                mime="text/csv",
                use_container_width=True,
            )
