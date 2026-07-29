"""Shop by category section matching Organic Mandya reference Image 2."""

import streamlit as st
from products import CATEGORIES
from utils.cart_manager import go_to


def render_categories(columns_per_row: int = 8):
    """Render 16 categories in an 8-column responsive grid matching Image 2."""
    
    st.markdown(
        """
        <div style="font-size: 0.85rem; font-weight: 800; color: #00472B; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px;">
            BROWSE
        </div>
        <div style="font-size: 2rem; font-weight: 800; color: #00472B; margin-bottom: 1.5rem;">
            Shop by category
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display Categories in rows of 8
    for row_start in range(0, len(CATEGORIES), columns_per_row):
        row_cats = CATEGORIES[row_start : row_start + columns_per_row]
        cols = st.columns(columns_per_row)
        
        for col, cat in zip(cols, row_cats):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #F3F6F3;
                        border-radius: 16px;
                        padding: 1rem 0.5rem;
                        text-align: center;
                        transition: transform 0.2s ease;
                        margin-bottom: 8px;
                    ">
                        <img src="{cat.image_url}" style="width: 100%; height: 95px; object-fit: cover; border-radius: 10px; margin-bottom: 6px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Category Name Clickable Button
                if st.button(cat.name, key=f"cat_grid_btn_{cat.slug}", use_container_width=True):
                    go_to("category", active_category=cat.slug)
                    st.rerun()

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)