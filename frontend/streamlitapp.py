"""
streamlitapp.py — entry point, routing และ sidebar
Run: streamlit run frontend/streamlitapp.py
"""

import sys
import os

# Ensure root path is available
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import requests

# -----------------------------------------------------------------------------
# 🔥 INTERNAL DEBUG ROUTES (HF WORKAROUND)
# MUST BE BEFORE ANY UI RENDERING
# -----------------------------------------------------------------------------

# Safe query params (compatible with all Streamlit versions)
try:
    query_params = st.query_params
except Exception:
    query_params = st.experimental_get_query_params()

# -----------------------------------------------------------------------------
# HEALTH CHECK ROUTE
# -----------------------------------------------------------------------------
if query_params.get("health") == "1":
    try:
        r = requests.get("http://127.0.0.1:8000/health", timeout=2)
        st.json(r.json())
    except Exception as e:
        st.error(f"Health check failed: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SWAGGER DOCS ROUTE
# -----------------------------------------------------------------------------
if query_params.get("docs") == "1":
    st.title("FastAPI Docs")

    st.components.v1.iframe(
        "http://127.0.0.1:8000/docs",
        height=900,
        scrolling=True
    )
    st.stop()

# -----------------------------------------------------------------------------
# NORMAL APP STARTS HERE
# -----------------------------------------------------------------------------

from frontend.config import TIMEZONES, TRANSLATIONS
from frontend._data.api_client import is_api_alive

import frontend._pages.feed         as feed
import frontend._pages.market       as market
import frontend._pages.topics       as topics
import frontend._pages.geopolitical as geo
import frontend._pages.qa           as qa
import frontend._pages.dev          as dev

# -----------------------------------------------------------------------------
# STREAMLIT CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TrumpSignal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📊 TrumpSignal")

    # Default language (you can extend later)
    T = TRANSLATIONS["English"]

    # Timezone selector
    tz_label = st.selectbox(
        T["timezone"],
        list(TIMEZONES.keys())
    )
    tz_offset = TIMEZONES[tz_label]

    st.divider()

    # Dashboard mode selector
    dashboard = st.radio(
        T["dashboard"],
        [T["nav_user"], T["nav_dev"]],
        index=0,
    )

    st.divider()

    # -----------------------------------------------------------------------------
    # API STATUS CHECK (SAFE)
    # -----------------------------------------------------------------------------
    try:
        api_ok = is_api_alive()
    except Exception:
        api_ok = False

    if api_ok:
        st.success(T["api_online"], icon="✅")
    else:
        st.warning(T["api_offline"], icon="⚠️")

    # Static info
    st.caption("Posts: daily · Geopolitical: weekly")

    # Version file (safe read)
    try:
        version_path = os.path.join(
            os.path.dirname(__file__),
            "VERSION"
        )
        version = open(version_path).read().strip()
    except Exception:
        version = "1.0.0"

    st.caption(f"v{version} — TrumpSignal")

# -----------------------------------------------------------------------------
# ROUTING
# -----------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # TABS
    # -------------------------------------------------------------------------
    with tab1:
        feed.render(T, tz_offset)

    with tab2:
        topics.render(T)

    with tab3:
        market.render(T)

    with tab4:
        geo.render(T)

    with tab5:
        qa.render(T)

else:
    dev.render(T)