"""
streamlitapp.py — entry point, routing และ sidebar
Run: streamlit run frontend/streamlitapp.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from frontend.config import LANGUAGES, TIMEZONES, TRANSLATIONS
from frontend._data.api_client import is_api_alive
import frontend._pages.feed         as feed
import frontend._pages.market       as market
import frontend._pages.topics       as topics
import frontend._pages.geopolitical as geo
import frontend._pages.qa           as qa
import frontend._pages.dev          as dev

st.set_page_config(
    page_title="TrumpSignal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 TrumpSignal")

    lang      = st.selectbox("Language / ภาษา / 语言", LANGUAGES)
    T         = TRANSLATIONS[lang]

    tz_label  = st.selectbox(T["timezone"], list(TIMEZONES.keys()))
    tz_offset = TIMEZONES[tz_label]

    st.divider()

    dashboard = st.radio(
        T["dashboard"],
        [T["nav_user"], T["nav_dev"]],
        index=0,
    )

    st.divider()

    # API status only — no empty nav items
    if is_api_alive():
        st.success(T["api_online"], icon="✅")
    else:
        st.warning(T["api_offline"], icon="⚠️")

    st.caption("Posts: daily · Geopolitical: weekly")
    st.caption("v0.1 — TrumpSignal")

# ── Route ─────────────────────────────────────────────────────────────────────
if dashboard == T["nav_user"]:
    st.title(T["app_title"])
    st.caption(T["tagline"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        T["daily_feed"],
        T["topics"],
        T["market"],
        T["geo"],
        T["qa"],
    ])

    with tab1: feed.render(T, tz_offset)
    with tab2: topics.render(T)
    with tab3: market.render(T)
    with tab4: geo.render(T)
    with tab5: qa.render(T)

else:
    dev.render(T)
