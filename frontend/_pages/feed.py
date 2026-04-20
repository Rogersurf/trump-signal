"""pages/feed.py — Daily feed with real ML prediction (graceful fallback)"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from frontend._data.api_client import get_posts
from frontend._components.post_card import _detect_topics, _get_effects
from backend_database.data_api import DB_PATH

STOCK_OPTIONS = {
    "all":   "All stocks",
    "sp500": "S&P 500",
    "qqq":   "QQQ (Nasdaq)",
    "djt":   "DJT (Trump Media)",
    "gld":   "GLD (Gold)",
    "tlt":   "TLT (US Bonds)",
    "lmt":   "LMT (Lockheed)",
    "uso":   "USO (Oil)",
    "ibit":  "IBIT (Bitcoin ETF)",
    "uup":   "UUP (US Dollar)",
    "war":   "WAR ETF",
}

ALL_STOCKS = {
    "sp500": "S&P 500",
    "qqq":   "QQQ",
    "djt":   "DJT",
    "gld":   "Gold",
    "tlt":   "Bonds",
    "lmt":   "LMT",
    "uso":   "Oil",
    "ibit":  "Bitcoin",
    "uup":   "Dollar",
    "war":   "WAR",
}

CAT_SIGNALS = {
    "Threatening intl.":    ("🔴", "-0.28%"),
    "Attacking opposition": ("🟠", "-0.09%"),
    "Self-promotion":       ("🔵", "+0.06%"),
    "Enacting non-agg.":    ("🟢", "+0.09%"),
    "Praising/endorsing":   ("🟢", "+0.04%"),
    "De-escalating":        ("🟢", "+0.11%"),
}

def _next_trading_day(d: date) -> date:
    next_day = d + timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    return next_day

def _is_xgboost_available() -> bool:
    """Check if xgboost is installed and importable."""
    try:
        import importlib.util
        return importlib.util.find_spec("xgboost") is not None
    except:
        return False

def _get_ml_prediction(selected_date: date) -> dict:
    """Get ML prediction via API endpoint."""
    try:
        import requests
        from frontend.config import API_URL
        r = requests.get(
            f"{API_URL}/model/predict/date/{selected_date}",
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            if "error" not in data:
                proba = float(data["next_day_impact_proba"])
                return {
                    "impact":     data["impact"],
                    "confidence": round(proba, 2),
                    "direction":  data["direction"],
                    "next_day":   _next_trading_day(selected_date),
                    "is_mock":    False,
                }
    except Exception:
        pass
    return None

def _get_clock(tz_offset: int) -> str:
    now = datetime.utcnow() + timedelta(hours=tz_offset)
    return now.strftime("%H:%M:%S")

def _get_market_status() -> tuple:
    et_now = datetime.utcnow() - timedelta(hours=4)
    is_weekday   = et_now.weekday() < 5
    market_open  = et_now.replace(hour=9,  minute=30, second=0)
    market_close = et_now.replace(hour=16, minute=0,  second=0)
    if is_weekday and market_open <= et_now <= market_close:
        return "🟢 Market open", "#1D9E75"
    return "🔴 Market closed", "#E24B4A"


def render(T: dict, tz_offset: int):
    # get dataset max date dynamically
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        ds_end = pd.to_datetime(conn.execute("SELECT MAX(date) FROM truth_social").fetchone()[0]).date()
        conn.close()
    except:
        ds_end = date.today()
    today  = min(date.today(), ds_end)

    # ── Live clock + market status ────────────────────────────────────────────
    clock_col, status_col, _ = st.columns([2, 2, 3])
    with clock_col:
        st.markdown(
            f'<p style="font-size:22px;font-weight:700;font-family:monospace;margin:0">'
            f'{_get_clock(tz_offset)}</p>'
            f'<p style="font-size:11px;color:#888;margin:0">UTC{tz_offset:+d}</p>',
            unsafe_allow_html=True,
        )
    with status_col:
        status_text, status_color = _get_market_status()
        st.markdown(
            f'<p style="font-size:14px;font-weight:600;color:{status_color};margin:8px 0 0">'
            f'{status_text}</p>'
            f'<p style="font-size:11px;color:#888;margin:0">NYSE / NASDAQ</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Controls ──────────────────────────────────────────────────────────────
    c1, c2 = st.columns([2, 2])
    with c1:
        selected_date = st.date_input(
            "Select date",
            key="feed_date",
            value=today,
            min_value=date(2022, 1, 1),
            max_value=ds_end,
            format="DD/MM/YYYY",
        )
    with c2:
        stock_key = st.selectbox(
            "Stock to track",
            options=list(STOCK_OPTIONS.keys()),
            format_func=lambda x: STOCK_OPTIONS[x],
        )

    # ── ML Prediction (graceful fallback) ─────────────────────────────────────
    pred = _get_ml_prediction(selected_date)
    next_td = _next_trading_day(selected_date)

    pred_box, _ = st.columns([3, 2])
    with pred_box:
        if pred:
            impact_color = "#E24B4A" if pred["impact"] == "HIGH" else "#1D9E75"
            dir_arrow    = "▲" if pred["direction"] == "UP" else "▼"
            dir_color    = "#1D9E75" if pred["direction"] == "UP" else "#E24B4A"
            st.markdown(
                f'<div style="background:#f8f6f1;border-radius:8px;padding:14px;margin-bottom:12px">'
                f'<p style="font-size:11px;color:#888;margin:0 0 4px">📊 ML prediction based on all posts from {selected_date.strftime("%d %b %Y")}</p>'
                f'<span style="font-size:22px;font-weight:700;color:{impact_color}">{pred["impact"]} IMPACT</span>'
                f'&nbsp;&nbsp;'
                f'<span style="font-size:18px;font-weight:600;color:{dir_color}">{dir_arrow} {pred["direction"]}</span>'
                f'<p style="font-size:12px;margin:4px 0 0">Probability: <b>{pred["confidence"]*100:.0f}%</b> · '
                f'Predicting for: <b>{next_td.strftime("%a, %d %b %Y")}</b></p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info(
                f"📊 ML prediction model is being trained. "
                f"Showing real post data for {selected_date.strftime('%d %b %Y')}."
            )

    # ── Posts ─────────────────────────────────────────────────────────────────
    posts = get_posts(str(selected_date), str(selected_date))

    if posts.empty:
        if selected_date == today:
            st.info("🕐 Trump hasn't posted anything today yet.")
        else:
            st.info(f"📭 Trump didn't post anything on {selected_date.strftime('%d %b %Y')}.")
        return

    st.caption(f"{len(posts)} posts · UTC{tz_offset:+d} · tracking {STOCK_OPTIONS[stock_key]}")

    for _, row in posts.iterrows():
        # Safely extract values with defaults
        text = str(row.get("text", "")) if pd.notna(row.get("text")) else ""
        category = row.get("dominant_category", "Other")
        if pd.isna(category) or not category:
            category = "Other"

        # Handle datetime safely
        dt_val = row.get("datetime")
        try:
            dt_obj = pd.to_datetime(dt_val)
            time_str = (dt_obj + timedelta(hours=tz_offset)).strftime("%d/%m/%Y %H:%M")
        except:
            time_str = str(row.get("date", ""))

        # Engagement metrics with safe defaults
        favs = int(row.get("favourites", 0) or 0)
        reblogs = int(row.get("reblogs", 0) or 0)
        replies = int(row.get("replies", 0) or 0)

        # Stock impact
        if stock_key == "all":
            stock_impacts = {}
            for sk, sl in ALL_STOCKS.items():
                try:
                    b = float(row.get(f"{sk}_5min_before", 0) or 0)
                    a = float(row.get(f"{sk}_5min_after", 0) or 0)
                    if b != 0:
                        stock_impacts[sl] = round((a - b) / b * 100, 2)
                except:
                    pass
            impact_str = "multiple"
            impact_color = "#888"
        else:
            stock_impacts = {}
            try:
                b = float(row.get(f"{stock_key}_5min_before", row.get("sp500_5min_before", 0)) or 0)
                a = float(row.get(f"{stock_key}_5min_after", row.get("sp500_5min_after", 0)) or 0)
                impact = round((a - b) / b * 100, 2) if b != 0 else 0
                impact_str = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
                impact_color = "#1D9E75" if impact >= 0 else "#E24B4A"
            except:
                impact_str = "N/A"
                impact_color = "#888"

        topics = _detect_topics(text)
        effects = _get_effects(topics)

        with st.container(border=True):
            st.caption(time_str)
            st.markdown(
                f'<span style="background:#EEEDFE;color:#3C3489;padding:2px 8px;'
                f'border-radius:3px;font-size:11px">{category}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"> {text}" if text else "*[Media post — no text content]*")
            st.caption(f"❤️ {favs:,}  🔁 {reblogs:,}  💬 {replies:,}")

            if stock_key == "all" and stock_impacts:
                cols_s = st.columns(len(stock_impacts))
                for idx_s, (sl, sv) in enumerate(stock_impacts.items()):
                    col_s = "#1D9E75" if sv >= 0 else "#E24B4A"
                    cols_s[idx_s].markdown(
                        f'<p style="font-size:11px;margin:0;color:#888">{sl}</p>'
                        f'<p style="font-size:13px;font-weight:700;margin:0;color:{col_s}">'
                        f'{sv:+.2f}%</p>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f'<p style="font-weight:700;font-size:13px;color:{impact_color};margin:4px 0">'
                    f'{STOCK_OPTIONS[stock_key]} {impact_str} after post</p>',
                    unsafe_allow_html=True,
                )
            if topics:
                st.caption("Topics: " + " · ".join(topics))
            if effects:
                st.caption("May affect: " + " · ".join(effects[:2]))
            if category in CAT_SIGNALS:
                icon, avg = CAT_SIGNALS[category]
                st.info(f"{icon} Category avg: S&P {avg} in 5 min")