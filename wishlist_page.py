"""Wishlist page: saved favorite items with one-click Add to Cart."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import (
    wishlist_items, remove_from_wishlist, add_to_cart, go_to
)


def render_wishlist_page():
    if st.button("← Continue shopping"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="om-section-title">Your Saved Wishlist ❤️</div>', unsafe_allow_html=True)

    items = wishlist_items()
    if not items:
        st.info("Your wishlist is empty. Browse products on the home page and click 🤍 to save them!")
        return

    cols = st.columns(min(len(items), 4))
    for i, product in enumerate(items):
        with cols[i % 4]:
            st.markdown('<div class="om-product-card">', unsafe_allow_html=True)
            st.image(product.image_path, use_container_width=True)
            st.markdown(f"**{product.name}**")
            st.caption(f"📍 {product.farm_location}")
            st.markdown(f"**{CURRENCY} {product.price:,.2f}**")
            
            c_add, c_del = st.columns([3, 1])
            with c_add:
                if st.button("🛒 Add to Cart", key=f"wish_add_{product.id}", use_container_width=True):
                    add_to_cart(product, variant=product.variants[0], qty=1)
                    st.toast(f"Moved {product.name} to cart! 🎉")
                    st.rerun()
            with c_del:
                if st.button("🗑️", key=f"wish_rm_{product.id}", use_container_width=True):
                    remove_from_wishlist(product.id)
                    st.toast("Removed from wishlist")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
