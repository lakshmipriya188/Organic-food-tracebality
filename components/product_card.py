"""Product card component displaying clean price, discount badge, wishlist action, and icons from product_icons folder."""

import os
import streamlit as st
from config import CURRENCY
from utils.cart_manager import add_to_cart, is_in_wishlist, toggle_wishlist
from utils.image_utils import get_image_src


def render_product_card(product, key_prefix: str = "prod"):
    """Render a modern product card with discount, original price, final price, wishlist button, and no trace button."""
    
    in_wish = is_in_wishlist(product.id)
    heart_symbol = "❤️" if in_wish else "♡"
    
    # Target image file path for native Streamlit rendering or base64 fallback
    image_target = product.image_url if (product.image_url and os.path.exists(product.image_url)) else get_image_src(product.image_url)

    with st.container():
        # Discount Badge top-left
        if product.discount_pct and product.discount_pct > 0:
            st.markdown(
                f"""
                <div style="
                    display: inline-block;
                    background: linear-gradient(135deg, #E11D48 0%, #BE123C 100%);
                    color: #FFFFFF;
                    font-size: 0.72rem;
                    font-weight: 800;
                    padding: 4px 10px;
                    border-radius: 20px;
                    margin-bottom: 6px;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 8px rgba(225, 29, 72, 0.25);
                ">
                    -{int(product.discount_pct)}% OFF
                </div>
                """,
                unsafe_allow_html=True
            )

        # Product Image (Rendered natively via st.image for 100% reliable display on screen)
        st.image(image_target, use_container_width=True)

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
                margin-top: 0.4rem;
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

        # Action Buttons Row: Add to Cart & Wishlist
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
