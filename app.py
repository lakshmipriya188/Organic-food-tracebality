"""Home page: hero banner + shop by category + customer favourites."""

import streamlit as st
from categories import render_categories
from favourites import render_favourites


def render_home_page():
    st.write("")
    render_categories()
    st.write("")
    render_favourites()
