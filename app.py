"""Main Streamlit Application for Organic Mandya - Classic Organic View."""

import streamlit as st
from utils.cart_manager import _init_state, go_to
from components.header import render_header
from components.footer import render_footer
from categories import render_categories
from favourites import render_favourites
from category_page import render_category_page
from cart_page import render_cart_page
from wishlist_page import render_wishlist_page
from login_page import render_login_page
from traceability_page import render_traceability_page
from pages.store_locations_page import render_store_locations_page
from pages.deals_page import render_deals_page
from pages.search_page import render_search_page


def inject_classic_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #FFFFFF;
            color: #0A3A2A;
        }

        /* Classic Typography Headings */
        h1, h2, h3, .classic-heading {
            font-family: 'Georgia', 'Playfair Display', serif !important;
            letter-spacing: -0.3px;
        }

        /* Streamlit Button Overrides */
        .stButton>button {
            border-radius: 10px;
            font-weight: 700;
            background-color: #00472B;
            color: #FFFFFF !important;
            border: none;
            padding: 0.5rem 1.2rem;
            transition: all 0.2s ease;
            box-shadow: 0 2px 5px rgba(0, 71, 43, 0.12);
        }
        .stButton>button:hover {
            background-color: #0F5233;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0, 71, 43, 0.2);
        }

        /* Inputs */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #D1D5DB;
            padding: 0.55rem 1rem;
        }

        /* Selectboxes */
        .stSelectbox>div>div {
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    st.set_page_config(
        page_title="Organic Mandya | Pure Roots",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    _init_state()
    inject_classic_styles()
    render_header()

    page = st.session_state.get("page", "home")

    if page == "home":
        render_categories()
        render_favourites()
    elif page == "category":
        render_category_page()
    elif page == "cart":
        render_cart_page()
    elif page == "wishlist":
        render_wishlist_page()
    elif page == "account" or page == "login":
        render_login_page()
    elif page == "traceability":
        render_traceability_page()
    elif page == "store_locations":
        render_store_locations_page()
    elif page == "deals":
        render_deals_page()
    elif page == "search":
        render_search_page()
    else:
        render_categories()
        render_favourites()

    render_footer()


if __name__ == "__main__":
    main()
