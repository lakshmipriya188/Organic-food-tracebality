"""'Shop by category' grid section."""

import streamlit as st
from products import CATEGORIES
from utils.cart_manager import go_to


def render_categories(columns_per_row: int = 8):
    st.markdown('<div class="om-section-heading">BROWSE</div>', unsafe_allow_html=True)
    st.markdown('<div class="om-section-title">Shop by category</div>', unsafe_allow_html=True)

    for row_start in range(0, len(CATEGORIES), columns_per_row):
        row = CATEGORIES[row_start:row_start + columns_per_row]
        cols = st.columns(columns_per_row)
        for col, cat in zip(cols, row):
            with col:
                st.markdown('<div class="om-cat-card">', unsafe_allow_html=True)
                st.image(cat.image_path, use_container_width=True)
                st.markdown(f'<div class="om-cat-label">{cat.name}</div>', unsafe_allow_html=True)
                if st.button("View", key=f"cat_view_{cat.slug}", use_container_width=True):
                    go_to("category", active_category=cat.slug)
                st.markdown('</div>', unsafe_allow_html=True)
    st.write("")