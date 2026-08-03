"""Shop by category section displaying categories loaded dynamically from MySQL Category table."""

import streamlit as st
from products import get_all_categories
from utils.cart_manager import go_to
from utils.image_utils import get_image_src


def render_categories(columns_per_row: int = 5):
    """Render categories in a clean grid loaded from MySQL Category table."""
    categories = get_all_categories()

    st.markdown(
        """
        <div style="font-family: 'Poppins', sans-serif; font-size: 0.82rem; font-weight: 700; color: #16A34A; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">
            BROWSE CATEGORIES
        </div>
        <div style="font-family: 'Poppins', sans-serif; font-size: 2rem; font-weight: 700; color: #1B4D3E; margin-bottom: 1.5rem;">
            Shop by Organic Category 🌿
        </div>
        """,
        unsafe_allow_html=True
    )

    if not categories:
        st.info("No categories found in the database.")
        return

    # Display Categories in rows
    for row_start in range(0, len(categories), columns_per_row):
        row_cats = categories[row_start : row_start + columns_per_row]
        cols = st.columns(columns_per_row)
        
        for col, cat in zip(cols, row_cats):
            img_src = get_image_src(cat.image_url)
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #FFFFFF;
                        border-radius: 18px;
                        padding: 0.9rem;
                        text-align: center;
                        border: 1px solid #E2E9E3;
                        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
                        margin-bottom: 10px;
                        transition: transform 0.25s ease, box-shadow 0.25s ease;
                        height: 140px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        overflow: hidden;
                    ">
                        <img src="{img_src}" style="
                            width: 100%;
                            height: 120px;
                            object-fit: cover;
                            border-radius: 12px;
                            transition: transform 0.3s ease;
                        ">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Category Name Clickable Button
                if st.button(cat.name, key=f"cat_grid_btn_{cat.category_id}_{cat.slug}", use_container_width=True):
                    st.session_state["active_category_id"] = cat.category_id
                    go_to("category", active_category=cat.slug)
                    st.rerun()

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)