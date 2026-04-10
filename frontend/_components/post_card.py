"""
components/post_card.py
=======================
Post card component — ใช้ซ้ำได้ใน feed และ Q&A
"""

import streamlit as st
from datetime import timedelta
from frontend.config import CATEGORY_COLORS, SENTIMENT_COLORS

KEYWORD_MAP = {
    "Iran":      ["iran", "strait", "hormuz", "tehran", "persian"],
    "Economy":   ["jobs", "trade deficit", "tariff", "economy", "gdp", "inflation", "market"],
    "Military":  ["strike", "military", "colonel", "rescue", "force", "troops", "nato"],
    "China":     ["china", "chinese", "beijing", "xi", "taiwan", "fentanyl"],
    "Politics":  ["caucus", "congress", "democrat", "republican", "senate", "election"],
    "Energy":    ["oil", "gas", "energy", "opec", "pipeline", "drilling"],
    "Immigration": ["border", "immigration", "migrants", "illegal", "deportation"],
}

EFFECT_MAP = {
    "Iran":       ["🛢️ Oil & energy prices", "✈️ Defense stocks (LMT, RTX)", "🌍 Middle East ETFs"],
    "Economy":    ["📈 US equities broadly", "💵 USD strength", "📊 Treasury yields"],
    "Military":   ["✈️ Defense stocks", "🛢️ Oil prices", "🌍 Emerging market risk"],
    "China":      ["📦 Supply chain stocks", "🌏 Asia-Pacific ETFs (FXI)", "💹 Tech sector"],
    "Politics":   ["📊 General market sentiment", "🏛️ Healthcare & pharma", "💰 Tax-sensitive sectors"],
    "Energy":     ["🛢️ Oil ETFs (USO)", "⚡ Energy sector (XLE)", "💵 Petrodollar currencies"],
    "Immigration":["🏗️ Construction & labor", "🌽 Agriculture sector", "📊 Consumer spending"],
}

def _detect_topics(text: str) -> list:
    text_lower = text.lower()
    return [topic for topic, kws in KEYWORD_MAP.items()
            if any(kw in text_lower for kw in kws)]

def _get_effects(topics: list) -> list:
    effects = []
    for t in topics:
        effects.extend(EFFECT_MAP.get(t, []))
    return list(dict.fromkeys(effects))[:5] or ["📊 General market sentiment"]

def render_post_card(row: dict, T: dict, tz_offset: int = 0, show_detail: bool = True):
    """
    render โพสต์ 1 ใบ
    row: dict หรือ pd.Series ของ post
    T: translation dict
    tz_offset: timezone offset hours
    show_detail: แสดง impact analysis ใน expander หรือเปล่า
    """
    sentiment   = row.get("sentiment", "NEUTRAL")
    category    = row.get("dominant_category", "Other")
    impact      = row.get("market_impact_pct", 0.0)
    score       = row.get("sentiment_score", 0.0)
    engagement  = row.get("engagement_score", 0)

    sent_color  = SENTIMENT_COLORS.get(sentiment, "#888780")
    sent_icon   = "🟢" if sentiment == "POSITIVE" else ("🔴" if sentiment == "NEGATIVE" else "⚪")
    impact_str  = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
    impact_col  = "green" if impact >= 0 else "red"

    # Timezone adjust
    try:
        post_dt  = row["datetime"] + timedelta(hours=tz_offset)
        time_str = post_dt.strftime("%d/%m/%Y %H:%M")
    except:
        time_str = str(row.get("date", ""))

    label = f"**{time_str}** · {sent_icon} {sentiment} · :{impact_col}[S&P {impact_str}]"

    with st.expander(label, expanded=False):
        # ── Post text ─────────────────────────────────────────────
        st.markdown(f"> {row.get('text', '')}")
        st.divider()

        # ── Metrics row ───────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(T["sentiment"],  f"{score*100:.0f}%")
        c2.metric(T["category"],   category)
        c3.metric(T["engagement"], f"{engagement:,}")
        c4.metric(T["sp500_after"], impact_str,
                  delta_color="normal" if impact >= 0 else "inverse")

        st.caption(
            f"❤️ {row.get('favourites', 0):,} {T['likes']}  ·  "
            f"🔁 {row.get('reblogs', 0):,} {T['shares']}  ·  "
            f"💬 {row.get('replies', 0):,} {T['replies']}"
        )

        if not show_detail:
            return

        # ── Impact analysis ───────────────────────────────────────
        st.divider()
        st.markdown(f"#### {T['post_detail']}")

        topics  = _detect_topics(row.get("text", ""))
        effects = _get_effects(topics)

        if topics:
            st.markdown(
                f"**{T['post_mentions']}:** " +
                "  ·  ".join([f"`{t}`" for t in topics])
            )

        st.markdown(f"**{T['post_effects']}**")
        for e in effects:
            st.markdown(f"- {e}")

        # Category context
        cat_impacts = {
            "Threatening intl.":    ("🔴", "Historically correlates with S&P -0.28% avg in 5 min"),
            "Attacking opposition": ("🟠", "Minor negative market correlation, avg -0.09%"),
            "Self-promotion":       ("🟢", "Slight positive signal, avg +0.06%"),
            "Enacting non-agg.":    ("🟢", "Positive policy signal, avg +0.09%"),
            "Praising/endorsing":   ("🟡", "Minimal market impact, avg +0.04%"),
            "De-escalating":        ("🟢", "Positive for risk assets"),
            "Other":                ("⚪", "No consistent market pattern"),
        }
        icon, context = cat_impacts.get(category, ("⚪", "No data"))
        st.info(f"{icon} **Category signal:** {context}")
