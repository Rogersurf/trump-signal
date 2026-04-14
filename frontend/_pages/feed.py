"""pages/feed.py"""
import streamlit as st
from datetime import datetime, date, timedelta
from frontend._data.api_client import get_posts
from frontend._components.post_card import _detect_topics, _get_effects

SENTIMENT_BADGE = {
    "POSITIVE": ("#EAF3DE", "#27500A"),
    "NEGATIVE": ("#FCEBEB", "#791F1F"),
    "NEUTRAL":  ("#F1EFE8", "#444441"),
}

STOCK_OPTIONS = {
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

CAT_SIGNALS = {
    "Threatening intl.":    ("🔴", "-0.28%"),
    "Attacking opposition": ("🟠", "-0.09%"),
    "Self-promotion":       ("🔵", "+0.06%"),
    "Enacting non-agg.":    ("🟢", "+0.09%"),
    "Praising/endorsing":   ("🟢", "+0.04%"),
    "De-escalating":        ("🟢", "+0.11%"),
}

def _next_trading_day(post_date: date) -> date:
    """Return next trading day after post_date"""
    next_day = post_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5=Sat, 6=Sun
        next_day += timedelta(days=1)
    return next_day

def _mock_ml(text, category):
    """
    REPLACE: GET {API_URL}/predict?text=...&stock=...
    Returns: {"impact": "HIGH"/"LOW", "confidence": float, "direction": "UP"/"DOWN"}
    """
    import random, hashlib
    random.seed(int(hashlib.md5(text[:20].encode()).hexdigest()[:8], 16))
    high_cats = ["Threatening intl.", "Attacking opposition", "Enacting non-agg."]
    impact    = "HIGH" if category in high_cats else "LOW"
    direction = "DOWN" if category in ["Threatening intl.", "Attacking opposition"] else "UP"
    return {
        "impact":     impact,
        "confidence": round(random.uniform(0.55, 0.85), 2),
        "direction":  direction,
    }

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
    today    = date.today()
    ds_end   = date(2026, 4, 14)  # dataset max date

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
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        selected_date = st.date_input(
            "Select date",
            key="feed_date",
            value=min(today, ds_end),
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
    with c3:
        sentiment_filter = st.multiselect(
            "Sentiment",
            options=["POSITIVE", "NEUTRAL", "NEGATIVE"],
            default=["POSITIVE", "NEUTRAL", "NEGATIVE"],
        )

    posts = get_posts(str(selected_date), str(selected_date))

    if posts.empty:
        if selected_date == min(today, ds_end):
            st.info("🕐 Trump hasn't posted anything today yet. Check back later or select a previous date.")
        else:
            st.info(f"📭 Trump did not post anything on {selected_date.strftime('%d %b %Y')}.")
        return

    # Apply sentiment filter
    if sentiment_filter:
        posts = posts[posts["sentiment"].isin(sentiment_filter)]

    if posts.empty:
        st.info("📭 No posts match the selected sentiment filter.")
        return

    st.caption(f"{len(posts)} posts · UTC{tz_offset:+d} · tracking {STOCK_OPTIONS[stock_key]}")

    for _, row in posts.iterrows():
        sentiment = row.get("sentiment", "NEUTRAL")
        category  = row.get("dominant_category", "Other")
        bg, fg    = SENTIMENT_BADGE.get(sentiment, ("#F1EFE8", "#444441"))
        text      = str(row.get("text", ""))

        # Stock impact
        try:
            b      = float(row.get(f"{stock_key}_5min_before", row.get("sp500_5min_before", 0)))
            a      = float(row.get(f"{stock_key}_5min_after",  row.get("sp500_5min_after",  0)))
            impact = round((a - b) / b * 100, 2) if b != 0 else 0
            impact_str   = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
            impact_color = "#1D9E75" if impact >= 0 else "#E24B4A"
        except:
            impact_str = "N/A"; impact_color = "#888"

        try:
            post_dt  = row["datetime"] + timedelta(hours=tz_offset)
            time_str = post_dt.strftime("%d/%m/%Y %H:%M")
            post_date = post_dt.date()
        except:
            time_str  = str(row.get("date", ""))
            post_date = start_date

        # Next trading day
        next_td = _next_trading_day(post_date)

        pred         = _mock_ml(text, category)
        impact_level = pred["impact"]
        confidence   = pred["confidence"]
        direction    = pred["direction"]
        impact_lv_color = "#E24B4A" if impact_level == "HIGH" else "#1D9E75"
        dir_arrow    = "▼" if direction == "DOWN" else "▲"
        dir_color    = "#E24B4A" if direction == "DOWN" else "#1D9E75"

        topics  = _detect_topics(text)
        effects = _get_effects(topics)

        with st.container(border=True):
            left, right = st.columns([3, 2])

            # ── Left: post ────────────────────────────────────────────────────
            with left:
                st.caption(time_str)
                st.markdown(
                    f'<span style="background:{bg};color:{fg};padding:2px 8px;border-radius:3px;'
                    f'font-size:11px;font-weight:600;text-transform:uppercase;margin-right:6px">'
                    f'{sentiment}</span>'
                    f'<span style="background:#EEEDFE;color:#3C3489;padding:2px 8px;'
                    f'border-radius:3px;font-size:11px">{category}</span>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"> {text}" if text else "*[Media post — no text content]*")
                st.caption(
                    f"❤️ {row.get('favourites',0):,}  "
                    f"🔁 {row.get('reblogs',0):,}  "
                    f"💬 {row.get('replies',0):,}"
                )
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

            # ── Right: ML prediction ──────────────────────────────────────────
            with right:
                st.markdown("**Next day market prediction**")
                st.markdown(
                    f'<p style="font-size:26px;font-weight:700;'
                    f'color:{impact_lv_color};margin:4px 0">'
                    f'{impact_level} IMPACT</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="font-size:18px;font-weight:600;'
                    f'color:{dir_color};margin:0 0 8px">'
                    f'{dir_arrow} {direction}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"Confidence: **{confidence*100:.0f}%**")
                st.markdown(
                    f"Predicting for: **{next_td.strftime('%a, %d %b %Y')}**"
                )
                st.caption(
                    "Weekend/holiday posts predict next trading day."
                    if post_date.weekday() >= 4
                    else ""
                )
                st.caption("⚠️ Mock — real ML model pending")
