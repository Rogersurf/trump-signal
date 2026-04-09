"""pages/feed.py — Daily feed tab"""
import streamlit as st
from datetime import datetime
from frontend.data.api_client import get_posts
from frontend.components.post_card import render_post_card

def render(T: dict, tz_offset: int):
    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input(T["select_date"], value=datetime(2026, 4, 1),
                                   min_value=datetime(2022, 1, 1),
                                   max_value=datetime(2026, 4, 6), format="DD/MM/YYYY")
    with c2:
        end_date = st.date_input(T["to"], value=datetime(2026, 4, 6),
                                 min_value=datetime(2022, 1, 1),
                                 max_value=datetime(2026, 4, 6), format="DD/MM/YYYY")

    posts = get_posts(str(start_date), str(end_date))

    if posts.empty:
        st.info(T["no_results"])
        return

    st.caption(f"Showing {len(posts)} posts · times in UTC{tz_offset:+d}")
    st.info(T["click_post"], icon="👆")

    for _, row in posts.iterrows():
        render_post_card(row.to_dict(), T, tz_offset)
