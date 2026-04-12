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

# ── Impact prediction — load Chenghao's model ────────────────────────────────
# Loads once, cached so we don't reload on every post render
_impact_cache: dict = {}   # post_id → impact_proba

def _load_impact_predictions(days: int = 30) -> dict:
    """
    Call predict_latest() from Chenghao's model_predict.py.
    Returns dict of {content_snippet → impact_proba} for quick lookup.
    Only runs on market-hours posts (model is trained on those only).
    Falls back to empty dict silently if model files not found yet.
    """
    global _impact_cache
    if _impact_cache:
        return _impact_cache
    try:
        from backend.model_predict import predict_latest
        df = predict_latest(days=days)
        # key by first 80 chars of content — matches what feed uses as text
        _impact_cache = {
            str(row.get("content", ""))[:80]: float(row.get("impact_proba", 0.0))
            for _, row in df.iterrows()
        }
    except FileNotFoundError:
        # Model not trained yet — silent fallback
        pass
    except Exception as e:
        print(f"[feed] impact model error: {e}")
    return _impact_cache


def _get_impact_badge(proba: float | None, during_market: bool) -> str:
    """
    Convert impact_proba to a badge string for display.
    Only meaningful for market-hours posts.
    """
    if not during_market:
        return ""
    if proba is None:
        return ""
    if proba >= 0.6:
        return "⚠️ HIGH IMPACT"
    elif proba >= 0.4:
        return "🟡 MODERATE"
    else:
        return "✅ LOW IMPACT"


def _get_impact_color(proba: float | None) -> str:
    if proba is None:
        return "#888"
    if proba >= 0.6:
        return "#E24B4A"
    elif proba >= 0.4:
        return "#BA7517"
    return "#1D9E75"


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
    c1, c2, c3 = st.columns([2, 2, 2])
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

    posts = get_posts(str(start_date), str(end_date))
    if posts.empty:
        st.info(T["no_results"])
        st.caption("Note: dataset covers up to April 2026. Select dates within that range.")
        return

    # Load impact predictions once for the whole feed
    impact_map = _load_impact_predictions(days=30)
    has_model  = bool(impact_map)

    st.caption(f"{len(posts)} posts · UTC{tz_offset:+d} · {STOCK_OPTIONS[stock_key]}")
    if has_model:
        st.caption("⚠️ Impact badge = XGBoost binary classifier · market-hours posts only · threshold ≥ 0.6")
    else:
        st.caption("ℹ️ Impact model not loaded — run `backend.model_training` first to enable predictions")

    for _, row in posts.iterrows():
        sentiment = row.get("sentiment", "NEUTRAL")
        category  = row.get("dominant_category", "Other")
        bg, fg    = SENTIMENT_BADGE.get(sentiment, ("#F1EFE8", "#444441"))
        text      = str(row.get("text", ""))

        # Historical stock impact (real data from dataset)
        try:
            b = float(row.get(f"{stock_key}_5min_before", row.get("sp500_5min_before", 0)))
            a = float(row.get(f"{stock_key}_5min_after",  row.get("sp500_5min_after",  0)))
            impact       = round((a - b) / b * 100, 2) if b != 0 else 0
            impact_str   = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
            impact_color = "#1D9E75" if impact >= 0 else "#E24B4A"
        except:
            impact_str = "N/A"; impact_color = "#888"

        try:
            time_str = (row["datetime"] + timedelta(hours=tz_offset)).strftime("%d/%m/%Y %H:%M")
        except:
            time_str = str(row.get("date", ""))

        # Binary impact prediction from Chenghao's XGBoost model
        during_market = bool(row.get("during_market_hours", False))
        text_key      = text[:80]
        proba         = impact_map.get(text_key, None)
        badge         = _get_impact_badge(proba, during_market)
        badge_color   = _get_impact_color(proba)

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

            # ── Right: ML impact prediction ───────────────────────────────────
            with right:
                st.markdown("**Market Impact Prediction**")

                if not during_market:
                    # Post outside market hours — model doesn't apply
                    st.markdown(
                        '<p style="color:#888;font-size:12px;margin:4px 0">'
                        '🕐 Posted outside market hours<br>'
                        'Impact prediction not applicable</p>',
                        unsafe_allow_html=True,
                    )
                elif proba is not None:
                    # Real prediction from XGBoost model
                    st.markdown(
                        f'<p style="font-size:26px;font-weight:700;color:{badge_color};margin:4px 0">'
                        f'{badge}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<p style="font-size:13px;color:#555;margin:2px 0">'
                        f'Probability: <b>{proba:.0%}</b></p>',
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        "XGBoost classifier · 5-min window · market-hours posts only · "
                        "HIGH = prob ≥ 60%"
                    )
                else:
                    # Market hours post but not in prediction window
                    st.markdown(
                        '<p style="color:#888;font-size:12px;margin:4px 0">'
                        '📊 Market hours post<br>'
                        'Outside prediction window</p>',
                        unsafe_allow_html=True,
                    )