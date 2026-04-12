"""pages/qa.py — Q&A tab with generalized business impact interpretation"""
import streamlit as st
from frontend._data.api_client import ask_question
from frontend._components.post_card import render_post_card
from frontend.config import SENTIMENT_COLORS

# ── Generalized interpretation engine ────────────────────────────────────────
# REPLACE: เปลี่ยนเป็น LLM call ผ่าน API เมื่อพร้อม
# GET {API_URL}/interpret?query=...&posts=[...]

_RULES = [
    {
        "topics":   ["iran", "strait", "hormuz", "tehran"],
        "contexts": ["business", "trade", "company", "invest", "affect", "impact", "export", "import"],
        "response": (
            "⚠️ **Business impact — Iran/Middle East:**\n\n"
            "Trump's posts about Iran show escalating military rhetoric. "
            "If you have business exposure in the region, monitor:\n"
            "- **Oil & shipping:** Hormuz Strait disruption would spike Brent crude and "
            "increase shipping insurance premiums significantly\n"
            "- **Defense sector:** LMT, RTX, NOC tend to rise on military escalation posts\n"
            "- **Regional currencies:** IRR, regional EM currencies face volatility\n"
            "- **S&P pattern:** 'Threatening intl.' posts historically average **-0.28%** "
            "on S&P 500 within 5 minutes\n\n"
            "Recommended: watch oil futures and energy ETFs (USO, XLE) the day after such posts."
        ),
    },
    {
        "topics":   ["tariff", "trade", "china", "chinese", "import", "export"],
        "contexts": ["business", "company", "supply", "manufacture", "affect", "impact"],
        "response": (
            "📦 **Business impact — Trade/Tariffs:**\n\n"
            "Trump's trade-related posts create supply chain uncertainty. Key signals:\n"
            "- **Positive trade posts** (deals, agreements) average **+0.09%** S&P in 5 min\n"
            "- **Threatening trade posts** create short-term volatility in manufacturing ETFs\n"
            "- **China-specific posts** move FXI (China ETF) and Asia-Pacific markets significantly\n\n"
            "If your business imports from China or exports to the US, watch for "
            "'Enacting non-agg.' category posts as signals of policy stabilization."
        ),
    },
    {
        "topics":   ["economy", "jobs", "gdp", "inflation", "fed", "interest"],
        "contexts": ["invest", "stock", "market", "business", "affect", "impact"],
        "response": (
            "📈 **Market signal — Economy posts:**\n\n"
            "Economic boast posts from Trump tend to be short-term positive signals:\n"
            "- Jobs/GDP posts average **+0.17%** S&P in 5 min\n"
            "- These posts are categorized as 'Enacting non-agg.' or 'Self-promotion'\n"
            "- Effect tends to fade within 1 hour as markets re-anchor to fundamentals\n\n"
            "Useful for: intraday traders watching political news flow."
        ),
    },
    {
        "topics":   ["stock", "market", "nasdaq", "s&p", "dow", "crypto", "bitcoin"],
        "contexts": ["invest", "trading", "portfolio", "affect", "impact", "buy", "sell"],
        "response": (
            "💹 **Investor signal:**\n\n"
            "Based on pattern analysis across Trump's posts:\n"
            "- **Highest market impact:** Threatening international posts (-0.28% avg)\n"
            "- **Most positive signal:** Policy/economy posts (+0.09% avg)\n"
            "- **Biggest individual mover:** DJT (Trump Media stock) reacts strongly to "
            "all post categories as it tracks Trump's personal brand\n\n"
            "Note: These are 5-minute correlations only. Not financial advice."
        ),
    },
]

def _interpret(query: str, results: list) -> str:
    q = query.lower()
    for rule in _RULES:
        has_topic   = any(t in q for t in rule["topics"])
        has_context = any(c in q for c in rule["contexts"])
        # also check matched post texts
        post_texts  = " ".join([r["post"].get("text", "").lower() for r in results])
        topic_in_posts = any(t in post_texts for t in rule["topics"])
        if (has_topic or topic_in_posts) and has_context:
            return rule["response"]
    return (
        "Here are the most relevant posts matching your question. "
        "Check the sentiment badge and category for context on how this type of "
        "post historically moves markets."
    )


# ── Render ────────────────────────────────────────────────────────────────────

def render(T: dict):
    st.caption(
        "Ask anything in plain language — including business impact questions. "
        "We search Trump's real posts for the closest matches."
    )

    query = st.text_input("", placeholder=T["ask_placeholder"], label_visibility="collapsed")

    col_btn, col_k = st.columns([1, 3])
    with col_btn:
        search = st.button(T["search_btn"], type="primary", use_container_width=True)
    with col_k:
        top_k = st.slider("Results", 2, 6, 3, label_visibility="visible")

    if search and query.strip():
        with st.spinner("Searching..."):
            results = ask_question(query.strip(), top_k=top_k)

        # --- TEMPORARY DEBUG (REMOVE AFTER FIX) ---
        st.subheader("DEBUG: Raw API Response")
        st.json(results)
        # -----------------------------------------

        if not results:
            st.warning("⚠️ Could not connect to search backend. Please ensure the API server is running.")
            return

        # Business interpretation
        interpretation = _interpret(query, results)
        st.markdown(interpretation)
        st.divider()

        st.caption(f"**{T['top_matches']}** for: *{query}*")

        for r in results:
            post  = r.get("post", {})
            score = r.get("score", 0.0)
            impact = post.get("market_impact_pct", 0.0)
            impact_str = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
            impact_col = "green" if impact >= 0 else "red"
            sent   = post.get("sentiment", "NEUTRAL")
            sent_icon = "🟢" if sent == "POSITIVE" else ("🔴" if sent == "NEGATIVE" else "⚪")

            with st.container(border=True):
                cols = st.columns([7, 1])
                with cols[0]:
                    st.markdown(post.get("text", ""))
                    st.caption(
                        f"{post.get('date', '')} · "
                        f"{sent_icon} {sent} · "
                        f"{post.get('dominant_category', '')} · "
                        f"S&P :{impact_col}[{impact_str}]"
                    )
                with cols[1]:
                    st.metric(T["match"], f"{score:.0f}%")