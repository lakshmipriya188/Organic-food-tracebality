"""Product card component displaying clean price, discount badge, wishlist action, and icons from product_icons folder."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import add_to_cart, is_in_wishlist, toggle_wishlist
from utils.image_utils import get_image_src


def render_product_card(product, key_prefix: str = "prod"):
    """Render a modern product card with discount, original price, final price, wishlist button, and no trace button."""
    
    in_wish = is_in_wishlist(product.id)
    heart_symbol = "❤️" if in_wish else "♡"
    img_src = get_image_src(product.image_url)

    with st.container():
        # Outer Card Wrapper
        st.markdown(
            f"""
            <div style="
                background-color: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.1rem;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
                box-shadow: 0 8px 20px rgba(27, 77, 62, 0.04);
                transition: all 0.25s ease;
            ">
            """,
            unsafe_allow_html=True
        )

        # Discount Badge top-left
        if product.discount_pct and product.discount_pct > 0:
            st.markdown(
                f"""
                <div style="
                    position: absolute;
                    top: 14px;
                    left: 14px;
                    background: linear-gradient(135deg, #E11D48 0%, #BE123C 100%);
                    color: #FFFFFF;
                    font-size: 0.72rem;
                    font-weight: 800;
                    padding: 4px 10px;
                    border-radius: 20px;
                    z-index: 2;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 8px rgba(225, 29, 72, 0.25);
                ">
                    -{int(product.discount_pct)}% OFF
                </div>
                """,
                unsafe_allow_html=True
            )

        # Product Icon Image Container
        st.markdown(
            f"""
            <div style="
                text-align: center;
                margin-bottom: 0.8rem;
                background: #F8FAF8;
                border-radius: 14px;
                padding: 0.6rem;
                border: 1px solid #EEF3EF;
                overflow: hidden;
            ">
                <img src="{img_src}" style="
                    width: 100%;
                    height: 150px;
                    object-fit: contain;
                    border-radius: 10px;
                    transition: transform 0.3s ease;
                ">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Product Title
        st.markdown(
            f"""
            <div style="
                font-family: 'Poppins', sans-serif;
                font-size: 0.95rem;
                font-weight: 600;
                color: #0F291E;
                line-height: 1.35;
                height: 2.6rem;
                overflow: hidden;
                margin-bottom: 0.4rem;
            ">
                {product.name}
            </div>
            """,
            unsafe_allow_html=True
        )

        unit_str = f"/{product.unit}" if getattr(product, "unit", None) else ""

        # Price Display (Original Price, Discounted Final Price & Savings)
        if product.original_price and product.original_price > product.price:
            savings = product.original_price - product.price
            price_html = f"""
            <div style="margin-bottom: 0.8rem; font-family: 'Poppins', sans-serif;">
                <div style="display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap;">
                    <span style="font-size: 1.2rem; font-weight: 700; color: #16A34A;">
                        {CURRENCY}{product.price:,.2f}<span style="font-size: 0.82rem; font-weight: 600; color: #166534;">{unit_str}</span>
                    </span>
                    <span style="font-size: 0.82rem; color: #889990; text-decoration: line-through; font-weight: 500;">
                        {CURRENCY}{product.original_price:,.2f}{unit_str}
                    </span>
                </div>
                <div style="font-size: 0.75rem; color: #15803D; font-weight: 600; margin-top: 2px;">
                    Save {CURRENCY}{savings:,.2f}{unit_str}
                </div>
            </div>
            """
        else:
            price_html = f"""
            <div style="margin-bottom: 0.8rem; font-family: 'Poppins', sans-serif;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #16A34A;">
                    {CURRENCY}{product.price:,.2f}<span style="font-size: 0.82rem; font-weight: 600; color: #166534;">{unit_str}</span>
                </div>
            </div>
            """
        st.markdown(price_html, unsafe_allow_html=True)

        # Variant Selector
        selected_variant = st.selectbox(
            "Variant",
            options=product.variants,
            key=f"{key_prefix}_var_{product.id}",
            label_visibility="collapsed"
        )

        # Action Buttons Row: Add to Cart & Wishlist (No Trace Button)
        col_add, col_wish = st.columns([1.1, 1])

        with col_add:
            if st.button("🛒 Add", key=f"{key_prefix}_add_{product.id}", use_container_width=True):
                add_to_cart(product, variant=selected_variant, qty=1)
                st.toast(f"Added {product.name} ({selected_variant}) to cart! 🎉")
                st.rerun()

        with col_wish:
            w_text = f"{heart_symbol} Saved" if in_wish else f"{heart_symbol} Wishlist"
            if st.button(w_text, key=f"{key_prefix}_wish_{product.id}", use_container_width=True):
                toggle_wishlist(product)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
