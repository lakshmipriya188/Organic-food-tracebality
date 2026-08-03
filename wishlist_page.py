"""Wishlist page: saved favorite items with one-click Add to Cart."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import (
    wishlist_items, remove_from_wishlist, add_to_cart, go_to
)
from utils.image_utils import get_image_src


def render_wishlist_page():
    if st.button("← Continue shopping"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            SAVED PRODUCE
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            Your Saved Wishlist ❤️
        </div>
        """,
        unsafe_allow_html=True
    )

    items = wishlist_items()
    if not items:
        st.info("Your wishlist is currently empty. Browse products on the home page and click 🤍 to save them!")
        return

    cols = st.columns(min(len(items), 4))
    for i, product in enumerate(items):
        img_src = get_image_src(product.image_url)
        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="
                    background: #FFFFFF;
                    border: 1px solid #E2E9E3;
                    border-radius: 18px;
                    padding: 1.2rem;
                    box-shadow: 0 8px 20px rgba(27, 77, 62, 0.04);
                    margin-bottom: 1rem;
                ">
                    <img src="{img_src}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 12px; margin-bottom: 10px;">
                    <div style="font-weight: 700; color: #0F291E; font-size: 0.96rem; margin-bottom: 4px;">{product.name}</div>
                    <div style="font-weight: 800; color: #1B4D3E; font-size: 1.15rem; margin-bottom: 12px;">{CURRENCY}{product.price:,.2f} / {getattr(product, 'unit', 'kg')}</div>
                """,
                unsafe_allow_html=True
            )
            
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
