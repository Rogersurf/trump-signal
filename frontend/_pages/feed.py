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

# Per-interval accuracy — shorter = more accurate
# REPLACE: use real backtested accuracy from ML model
INTERVAL_META = {
    "5 min":  {"key": "t5",  "accuracy": 0.68, "note": "High confidence — short window"},
    "10 min": {"key": "t10", "accuracy": 0.63, "note": "Good confidence"},
    "30 min": {"key": "t30", "accuracy": 0.57, "note": "Moderate — more uncertainty"},
    "60 min": {"key": "t60", "accuracy": 0.51, "note": "Low confidence — long window"},
}

def _mock_ml(text, category):
    """
    REPLACE: GET {API_URL}/predict?text=...&stock=...
    Must return: {t5, t10, t30, t60} as % change predictions
    """
    import random, hashlib
    random.seed(int(hashlib.md5(text[:20].encode()).hexdigest()[:8], 16))
    neg = ["Threatening intl.", "Attacking opposition"]
    m   = -1 if category in neg else 1
    return {
        "t5":  round(m * random.uniform(0.05, 0.25), 2),
        "t10": round(m * random.uniform(0.08, 0.35), 2),
        "t30": round(m * random.uniform(0.10, 0.50), 2),
        "t60": round(m * random.uniform(0.12, 0.65), 2),
    }

def _get_clock(tz_offset: int) -> str:
    now = datetime.utcnow() + timedelta(hours=tz_offset)
    return now.strftime("%H:%M:%S")

def _get_market_status(tz_offset: int) -> tuple:
    """Check if US market is open (9:30–16:00 ET = UTC-4)"""
    et_now = datetime.utcnow() - timedelta(hours=4)
    is_weekday = et_now.weekday() < 5
    market_open  = et_now.replace(hour=9,  minute=30, second=0)
    market_close = et_now.replace(hour=16, minute=0,  second=0)
    if is_weekday and market_open <= et_now <= market_close:
        return "🟢 Market open", "#1D9E75"
    return "🔴 Market closed", "#E24B4A"


def render(T: dict, tz_offset: int):
    today = date.today()

    # ── Live clock + market status ────────────────────────────────────────────
    clock_col, status_col, _ = st.columns([2, 2, 3])
    with clock_col:
        clock = _get_clock(tz_offset)
        st.markdown(
            f'<p style="font-size:22px;font-weight:700;font-family:monospace;margin:0">'
            f'{clock}</p>'
            f'<p style="font-size:11px;color:#888;margin:0">UTC{tz_offset:+d}</p>',
            unsafe_allow_html=True,
        )
    with status_col:
        status_text, status_color = _get_market_status(tz_offset)
        st.markdown(
            f'<p style="font-size:14px;font-weight:600;color:{status_color};margin:8px 0 0">'
            f'{status_text}</p>'
            f'<p style="font-size:11px;color:#888;margin:0">NYSE / NASDAQ</p>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Controls ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
    with c1:
        start_date = st.date_input(
            T["select_date"],
            value=today - timedelta(days=7),
            min_value=date(2022, 1, 1),
            max_value=today,
            format="DD/MM/YYYY",
        )
    with c2:
        end_date = st.date_input(
            T["to"],
            value=today,
            min_value=date(2022, 1, 1),
            max_value=today,
            format="DD/MM/YYYY",
        )
    with c3:
        stock_key = st.selectbox(
            "Stock to track",
            options=list(STOCK_OPTIONS.keys()),
            format_func=lambda x: STOCK_OPTIONS[x],
        )
    with c4:
        interval = st.radio(
            "ML prediction interval",
            options=list(INTERVAL_META.keys()),
            horizontal=True,
        )

    posts = get_posts(str(start_date), str(end_date))
    if posts.empty:
        st.info(T["no_results"])
        st.caption("Note: dataset covers up to April 2026. Select dates within that range.")
        return

    # Show interval accuracy info
    meta = INTERVAL_META[interval]
    acc  = meta["accuracy"] * 100
    acc_color = "#1D9E75" if acc >= 65 else "#BA7517" if acc >= 58 else "#E24B4A"
    st.markdown(
        f'<div style="background:#f8f6f1;border-radius:6px;padding:8px 14px;margin-bottom:12px;'
        f'display:inline-block">'
        f'Showing <b>{interval}</b> predictions · '
        f'Model accuracy: <b style="color:{acc_color}">{acc:.0f}%</b> · '
        f'<span style="color:#888">{meta["note"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.caption(f"{len(posts)} posts · UTC{tz_offset:+d} · {STOCK_OPTIONS[stock_key]}")

    for _, row in posts.iterrows():
        sentiment = row.get("sentiment", "NEUTRAL")
        category  = row.get("dominant_category", "Other")
        bg, fg    = SENTIMENT_BADGE.get(sentiment, ("#F1EFE8", "#444441"))
        text      = str(row.get("text", ""))

        # Stock impact
        try:
            b = float(row.get(f"{stock_key}_5min_before", row.get("sp500_5min_before", 0)))
            a = float(row.get(f"{stock_key}_5min_after",  row.get("sp500_5min_after",  0)))
            impact = round((a - b) / b * 100, 2) if b != 0 else 0
            impact_str   = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
            impact_color = "#1D9E75" if impact >= 0 else "#E24B4A"
        except:
            impact_str = "N/A"; impact_color = "#888"

        try:
            time_str = (row["datetime"] + timedelta(hours=tz_offset)).strftime("%d/%m/%Y %H:%M")
        except:
            time_str = str(row.get("date", ""))

        pred   = _mock_ml(text, category)
        pred_val = pred[meta["key"]]
        pred_color = "#1D9E75" if pred_val >= 0 else "#E24B4A"
        pred_arrow = "▲" if pred_val >= 0 else "▼"
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
                st.markdown(f"> {text}")
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
                st.markdown(f"**ML prediction · {interval}**")
                st.markdown(
                    f'<p style="font-size:28px;font-weight:700;color:{pred_color};margin:4px 0">'
                    f'{pred_arrow} {pred_val:+.2f}%</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"**{STOCK_OPTIONS[stock_key]}** in **{interval}**\n\n"
                    f"Model accuracy for this interval: "
                    f"**{acc:.0f}%**\n\n"
                    f"_{meta['note']}_"
                )

                # All intervals summary
                st.markdown("---")
                st.markdown("**All intervals**")
                for iv, iv_meta in INTERVAL_META.items():
                    v     = pred[iv_meta["key"]]
                    color = "#1D9E75" if v >= 0 else "#E24B4A"
                    arrow = "▲" if v >= 0 else "▼"
                    acc_v = iv_meta["accuracy"] * 100
                    is_selected = "**" if iv == interval else ""
                    st.markdown(
                        f'{is_selected}{iv}{is_selected} · '
                        f'<span style="color:{color};font-weight:600">{arrow} {v:+.2f}%</span> · '
                        f'<span style="color:#888;font-size:11px">acc {acc_v:.0f}%</span>',
                        unsafe_allow_html=True,
                    )

                st.caption("⚠️ Mock — real ML model pending")