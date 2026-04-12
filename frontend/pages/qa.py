"""pages/qa.py — Q&A tab with semantic search and market impact display"""
import streamlit as st
from frontend.data.api_client import ask_question


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
        top_k = st.slider("Results", 1, 10, 5, label_visibility="visible")

    if search and query.strip():
        with st.spinner("Searching..."):
            results = ask_question(query.strip(), top_k=top_k)

        if not results:
            st.info(T.get("no_results", "No results found. Try a different keyword."))
            return

        st.caption(f"{len(results)} posts found for: *{query}*")

        # Define stock tickers to display in the expander
        STOCKS = {
            "sp500": "S&P 500",
            "qqq": "QQQ (Nasdaq)",
            "djt": "DJT (Trump Media)",
            "gld": "GLD (Gold)",
            "tlt": "TLT (US Bonds)",
            "uso": "USO (Oil)",
            "ibit": "IBIT (Bitcoin ETF)",
            "lmt": "LMT (Lockheed)",
            "uup": "UUP (US Dollar)",
        }

        for i, r in enumerate(results, 1):
            post = r.get("post", {})
            score = r.get("score", 0.0)

            sent = post.get("sentiment", "NEUTRAL")
            sent_icon = "🟢" if sent == "POSITIVE" else ("🔴" if sent == "NEGATIVE" else "⚪")
            relevance = round(score, 0)  # score is already 0-100

            with st.container(border=True):
                # Header row
                h1, h2, h3 = st.columns([3, 2, 1])
                with h1:
                    st.caption(f"#{i} · {post.get('date', '')}")
                with h2:
                    st.markdown(f"{sent_icon} **{sent}** · {post.get('dominant_category', '')}")
                with h3:
                    st.markdown(
                        f'<p style="text-align:right;font-size:12px;color:#888;margin:0">Relevance</p>'
                        f'<p style="text-align:right;font-size:18px;font-weight:700;margin:0">{relevance:.0f}%</p>',
                        unsafe_allow_html=True,
                    )

                # Post text (handles media-only posts)
                text = post.get('text', '').strip()
                if text:
                    st.markdown(f"> {text}")
                else:
                    url = post.get('url', '')
                    st.markdown(
                        f'*[Media post — no text content]* '
                        f'{"· [View on Truth Social](" + url + ")" if url else ""}'
                    )

                # Market impact expander
                with st.expander("📊 Market impact — all stocks"):
                    for key, label in STOCKS.items():
                        before = post.get(f"{key}_5min_before")
                        after = post.get(f"{key}_5min_after")
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
                        except (TypeError, ValueError):
                            st.markdown(
                                f'<span style="display:inline-block;width:160px;'
                                f'color:#888;font-size:12px">{label}</span>'
                                f'<span style="color:#ccc;font-size:12px">N/A</span>',
                                unsafe_allow_html=True,
                            )