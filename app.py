"""Main Streamlit Application for Organic Foods - Premium Organic View."""

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

        /* Global Reset & Typography */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #F8FAF8;
            color: #0F291E;
        }

        .stApp {
            background-color: #F8FAF8;
        }

        /* Headings */
        h1, h2, h3, .classic-heading {
            font-family: 'Poppins', sans-serif !important;
            color: #1B4D3E !important;
            letter-spacing: -0.3px;
        }

        /* Streamlit Top Navigation & Padding Fix */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            height: 2.5rem !important;
            z-index: 1 !important;
        }

        .block-container {
            padding-top: 5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1280px !important;
        }

        /* Streamlit Button Overrides */
        .stButton>button {
            border-radius: 12px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 0.85rem;
            background: linear-gradient(135deg, #16A34A 0%, #15803D 100%);
            color: #FFFFFF !important;
            border: none;
            padding: 0.45rem 0.65rem;
            white-space: nowrap;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.2);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
            color: #FFFFFF !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
        }
        .stButton>button:active {
            transform: translateY(0);
        }

        /* Secondary & Form Buttons */
        div[data-testid="stForm"] .stButton>button,
        .stButton>button[kind="secondary"] {
            border-radius: 14px;
        }

        /* Text Inputs */
        .stTextInput>div>div>input {
            border-radius: 14px;
            border: 1.5px solid #E2E9E3;
            padding: 0.65rem 1.1rem;
            background-color: #FFFFFF;
            color: #0F291E;
            font-size: 0.92rem;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        }
        .stTextInput>div>div>input:focus {
            border-color: #16A34A;
            box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.15);
        }

        /* Selectboxes */
        .stSelectbox>div>div {
            border-radius: 14px;
            border: 1.5px solid #E2E9E3;
            background-color: #FFFFFF;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #F1F5F2;
        }
        ::-webkit-scrollbar-thumb {
            background: #A3B8AD;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #1B4D3E;
        }

        /* Cards & Section Containers */
        .of-card {
            background: #FFFFFF;
            border: 1px solid #E2E9E3;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease;
        }
        .of-card:hover {
            box-shadow: 0 12px 30px rgba(27, 77, 62, 0.08);
            transform: translateY(-3px);
        }

        .om-section-heading, .of-section-heading {
            font-size: 0.82rem;
            font-weight: 700;
            color: #16A34A;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 4px;
            font-family: 'Poppins', sans-serif;
        }
        .om-section-title, .of-section-title {
            font-size: 2rem;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
            color: #1B4D3E;
            margin-bottom: 1.4rem;
            line-height: 1.2;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #EDF3EE;
            padding: 6px;
            border-radius: 14px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: 10px;
            font-weight: 600;
            color: #4A6B5D;
            border: none;
            padding: 0 16px;
            font-family: 'Poppins', sans-serif;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #1B4D3E !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    st.set_page_config(
        page_title="Organic Foods | Pure Roots & 100% Organic",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    _init_state()
    inject_classic_styles()
    render_header()

    # Enforce Login Gate: User must be logged in to view store UI
    if not st.session_state.get("user"):
        render_login_page()
        render_footer()
        return

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
