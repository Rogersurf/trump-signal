"""pages/qa.py — Q&A tab with semantic search"""
import streamlit as st
from frontend._data.api_client import ask_question


def render(T: dict):
    st.caption("Search Trump's Truth Social posts by topic. Results ranked by relevance.")

    query = st.text_input(
        "Search",
        placeholder="Try: Iran, tariff, China, NATO, economy, bitcoin...",
        label_visibility="collapsed",
    )

    col_btn, col_k = st.columns([1, 3])
    with col_btn:
        search = st.button(T["search_btn"], type="primary", use_container_width=True)
    with col_k:
        top_k = st.slider("Results", 1, 10, 5, label_visibility="visible")

    if search and query.strip():
        with st.spinner("Searching..."):
            results = ask_question(query.strip(), top_k=top_k)

        if not results:
            st.info("No results found. Try a different keyword.")
            return

        st.caption(f"{len(results)} posts found for: *{query}*")

        for i, r in enumerate(results, 1):
            post       = r.get("post", {})
            score      = r.get("score", 0.0)
            impact     = post.get("market_impact_pct", 0.0)
            impact_str = f"+{impact:.2f}%" if impact >= 0 else f"{impact:.2f}%"
            impact_color = "#1D9E75" if impact >= 0 else "#E24B4A"

            relevance = round(score * 100, 0)

            with st.container(border=True):
                # ── Header row ────────────────────────────────────────────────
                h1, h2, h3 = st.columns([3, 2, 1])
                with h1:
                    url = post.get("url", "")
                    date_str = str(post.get("date", ""))[:10]
                    if url:
                        st.markdown(f"#{i} · {date_str} · [View on Truth Social]({url})")
                    else:
                        st.caption(f"#{i} · {date_str}")
                with h2:
                    st.markdown(
                        f"**{post.get('dominant_category', 'Other')}**",
                    )
                with h3:
                    st.markdown(
                        f'<p style="text-align:right;font-size:12px;color:#888;margin:0">Relevance</p>'
                        f'<p style="text-align:right;font-size:18px;font-weight:700;margin:0">{relevance:.0f}%</p>',
                        unsafe_allow_html=True,
                    )

                # ── Post text ─────────────────────────────────────────────────
                text = post.get('text', '').strip()
                if text:
                    st.markdown(f"> {text}")
                else:
                    url = post.get('url', '')
                    st.markdown(
                        f'*[Media post — no text content]* '
                        f'{"· [View on Truth Social](" + url + ")" if url else ""}'
                    )

                # ── Market impact dropdown ────────────────────────────────────
                STOCKS = {
                    "sp500": "S&P 500",
                    "qqq":   "QQQ (Nasdaq)",
                    "djt":   "DJT (Trump Media)",
                    "gld":   "GLD (Gold)",
                    "tlt":   "TLT (US Bonds)",
                    "uso":   "USO (Oil)",
                    "ibit":  "IBIT (Bitcoin ETF)",
                    "lmt":   "LMT (Lockheed)",
                    "uup":   "UUP (US Dollar)",
                }

                with st.expander("📊 Market impact — all stocks"):
                    for key, label in STOCKS.items():
                        before = post.get(f"{key}_5min_before", None)
                        after  = post.get(f"{key}_5min_after", None)
                        try:
                            b = float(before)
                            a = float(after)
                            chg = round((a - b) / b * 100, 2) if b != 0 else 0
                            chg_str = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
                            color = "#1D9E75" if chg >= 0 else "#E24B4A"
                            st.markdown(
                                f'<span style="display:inline-block;width:160px;'
                                f'color:#888;font-size:12px">{label}</span>'
                                f'<span style="font-weight:700;font-size:13px;'
                                f'color:{color}">{chg_str}</span>',
                                unsafe_allow_html=True,
                            )
                        except:
                            st.markdown(
                                f'<span style="display:inline-block;width:160px;'
                                f'color:#888;font-size:12px">{label}</span>'
                                f'<span style="color:#ccc;font-size:12px">N/A</span>',
                                unsafe_allow_html=True,
                            )