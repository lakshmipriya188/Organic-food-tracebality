"""Classic Product card component matching clean organic aesthetic."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import add_to_cart, is_in_wishlist, toggle_wishlist, go_to


def render_product_card(product, key_prefix: str = "fav"):
    """Render a clean classic product card."""
    
    in_wish = is_in_wishlist(product.id)
    heart_symbol = "❤️" if in_wish else "🤍"

    with st.container():
        # Outer Card Container
        st.markdown(
            f"""
            <div style="
                background-color: #F8FAF8;
                border: 1px solid #E5EBE5;
                border-radius: 16px;
                padding: 1.2rem;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
                box-shadow: 0 2px 8px rgba(0, 71, 43, 0.03);
            ">
            """,
            unsafe_allow_html=True
        )

        # Optional Discount Badge top-left
        if product.discount_pct:
            st.markdown(
                f"""
                <div style="
                    position: absolute;
                    top: 12px;
                    left: 12px;
                    background-color: #D9381E;
                    color: #FFFFFF;
                    font-size: 0.72rem;
                    font-weight: 800;
                    padding: 2px 8px;
                    border-radius: 6px;
                    z-index: 2;
                ">
                    -{product.discount_pct}%
                </div>
                """,
                unsafe_allow_html=True
            )

        # Product Image
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 0.8rem; background: #FFFFFF; border-radius: 12px; padding: 0.8rem; border: 1px solid #F0F4F1;">
                <img src="{product.image_url}" style="width: 100%; height: 160px; object-fit: contain; border-radius: 8px;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Product Title
        st.markdown(
            f"""
            <div style="
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 0.95rem;
                font-weight: 700;
                color: #0A3A2A;
                line-height: 1.35;
                height: 2.7rem;
                overflow: hidden;
                margin-bottom: 0.6rem;
            ">
                {product.name}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Main Price & Optional Strikethrough
        if product.original_price:
            price_html = f"""
            <div style="font-size: 1.2rem; font-weight: 800; color: #00472B; margin-bottom: 0.8rem;">
                {CURRENCY} {product.price:,.2f} 
                <span style="font-size: 0.85rem; color: #888888; text-decoration: line-through; margin-left: 6px;">
                    {CURRENCY} {product.original_price:,.2f}
                </span>
            </div>
            """
        else:
            price_html = f"""
            <div style="font-size: 1.2rem; font-weight: 800; color: #00472B; margin-bottom: 0.8rem;">
                {CURRENCY} {product.price:,.2f}
            </div>
            """
        st.markdown(price_html, unsafe_allow_html=True)

        # Variant Selector & Add Button Row
        c_var, c_add = st.columns([1, 1])

        with c_var:
            selected_variant = st.selectbox(
                "Variant",
                options=product.variants,
                key=f"{key_prefix}_var_{product.id}",
                label_visibility="collapsed"
            )

        with c_add:
            if st.button("Add", key=f"{key_prefix}_add_{product.id}", use_container_width=True):
                add_to_cart(product, variant=selected_variant, qty=1)
                st.toast(f"Added {product.name} ({selected_variant}) to cart! 🎉")
                st.rerun()

        # Secondary Actions Row (Wishlist & Traceability)
        c_w, c_t = st.columns([1, 1])
        with c_w:
            w_text = f"{heart_symbol} Saved" if in_wish else "♡ Wishlist"
            if st.button(w_text, key=f"{key_prefix}_wish_{product.id}", use_container_width=True):
                toggle_wishlist(product)
                st.rerun()

        with c_t:
            if st.button("🔍 Trace", key=f"{key_prefix}_trc_{product.id}", use_container_width=True):
                go_to("traceability", active_category=product.category_slug)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
