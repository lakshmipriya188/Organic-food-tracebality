"""Wishlist page: saved favorite items with cart-like features, quantity adjustment, price breakdowns, and DB sync."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import (
    wishlist_items, update_wishlist_qty, remove_from_wishlist,
    add_to_cart, clear_wishlist, go_to
)
from utils.image_utils import get_image_src


def render_wishlist_page():
    # Top action bar
    top_col1, _ = st.columns([1.5, 4])
    with top_col1:
        if st.button("← Continue Shopping", key="wish_continue_top", use_container_width=True):
            go_to("home")
            st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-top:0.8rem; margin-bottom:4px;">
            SAVED ORGANIC PRODUCE
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            Your Saved Wishlist ❤️
        </div>
        """,
        unsafe_allow_html=True
    )

    items = wishlist_items()

    if not items:
        st.info("Your wishlist is empty. Browse products on the home page and save your favorite organic items!")
        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        btn_c1, _ = st.columns([1, 1])
        with btn_c1:
            if st.button("← Continue Shopping", key="wish_continue_empty", use_container_width=True):
                go_to("home")
                st.rerun()
        return

    # Total accumulators
    total_mrp = 0.0
    total_discount = 0.0

    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size:1.15rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;'>Wishlist Items</div>", unsafe_allow_html=True)

    for item in items:
        product = item["product"]
        qty = item.get("qty", 1)
        item_key = item.get("key", f"{product.id}_1kg")
        variant = item.get("variant", "1kg")
        img_src = get_image_src(product.image_url)

        # Calculate item price components
        mrp_per_unit = float(product.original_price) if getattr(product, 'original_price', None) and product.original_price > product.price else float(product.price)
        disc_pct = float(getattr(product, 'discount_pct', 0.0) or 0.0)
        disc_amt_per_unit = round((mrp_per_unit * disc_pct) / 100.0, 2)
        final_price_per_unit = round(mrp_per_unit - disc_amt_per_unit, 2)

        item_total_mrp = mrp_per_unit * qty
        item_total_discount = disc_amt_per_unit * qty
        item_final_total = final_price_per_unit * qty

        total_mrp += item_total_mrp
        total_discount += item_total_discount

        category_name = getattr(product, 'category_name', None) or product.category_slug.title()
        p_unit = getattr(product, 'unit', 'kg')

        # Clean White Card Layout (Replica of Cart layout)
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.4rem;
                margin-bottom: 1.2rem;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            ">
            """,
            unsafe_allow_html=True
        )

        col_img, col_details, col_qty, col_actions = st.columns([1.2, 3.8, 2.2, 1.8])

        with col_img:
            st.markdown(
                f"""
                <img src="{img_src}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 12px; border: 1px solid #F0F4F1;">
                """,
                unsafe_allow_html=True
            )

        with col_details:
            st.markdown(f"<div style='font-family:\"Poppins\", sans-serif; font-weight:700; font-size:1.1rem; color:#0F291E; margin-bottom: 4px;'>{product.name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.85rem; color:#4A6B5D; margin-bottom: 8px;'>Category: <b>{category_name}</b> | Base Unit: <b>{p_unit}</b> | Variant: <b>{variant}</b></div>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style="font-size:0.88rem; color:#0F291E; line-height:1.6;">
                    <div>Price Before Discount: <b>{CURRENCY}{mrp_per_unit:,.2f}</b> / {p_unit}</div>
                    <div>Discount (%): <b>{int(disc_pct)}%</b></div>
                    <div>Discount Amount: <b>{CURRENCY}{disc_amt_per_unit:,.2f}</b> / {p_unit}</div>
                    <div>Final Price (after discount): <b>{CURRENCY}{final_price_per_unit:,.2f}</b> / {p_unit}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_qty:
            st.markdown(f"<div style='font-size:0.85rem; color:#0F291E; font-weight:600; margin-bottom:6px;'>Quantity ({p_unit})</div>", unsafe_allow_html=True)

            q_minus, q_val, q_plus = st.columns([1, 1.2, 1])
            with q_minus:
                if st.button("➖", key=f"w_dec_{item_key}", use_container_width=True):
                    update_wishlist_qty(item_key, qty - 1, product_id=product.id)
                    st.rerun()
            with q_val:
                st.markdown(f"<div style='text-align:center; font-weight:700; font-size:1.1rem; padding-top:6px; color:#0F291E;'>{qty} {p_unit}</div>", unsafe_allow_html=True)
            with q_plus:
                if st.button("➕", key=f"w_inc_{item_key}", use_container_width=True):
                    update_wishlist_qty(item_key, qty + 1, product_id=product.id)
                    st.rerun()

            st.markdown(f"<div style='font-size:0.82rem; color:#0F291E; margin-top:8px; text-align:center;'>Subtotal: <b>{CURRENCY}{item_final_total:,.2f}</b></div>", unsafe_allow_html=True)

        with col_actions:
            st.write("")
            if st.button("🛒 Move to Cart", key=f"w_move_{item_key}", use_container_width=True, type="primary"):
                add_to_cart(product, variant=variant, qty=qty)
                remove_from_wishlist(item_key, product_id=product.id)
                st.toast(f"Moved {product.name} to Cart! 🎉")
                st.rerun()

            if st.button("🗑️ Remove", key=f"w_rm_{item_key}", use_container_width=True):
                remove_from_wishlist(item_key, product_id=product.id)
                st.toast(f"Removed {product.name} from wishlist")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    final_payable = max(0.0, total_mrp - total_discount)

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)

    # Price Summary Section
    st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size:1.3rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;'>Wishlist Summary</div>", unsafe_allow_html=True)

    col_summary_details, col_final_highlight = st.columns([1.5, 1])

    with col_summary_details:
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E9E3;
                border-radius: 18px;
                padding: 1.5rem;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
            ">
                <div style="display:flex; justify-content:space-between; margin-bottom: 10px; font-size: 1rem; color: #0F291E;">
                    <span>Total MRP (Price Before Discount):</span>
                    <b>{CURRENCY}{total_mrp:,.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 10px; font-size: 1rem; color: #0F291E;">
                    <span>Total Discount Savings:</span>
                    <b style="color: #0F291E;">- {CURRENCY}{total_discount:,.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 4px; font-size: 0.88rem; color: #4A6B5D;">
                    <span>Calculation:</span>
                    <span>Total MRP − Total Discount</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_final_highlight:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #DCFCE7 0%, #F0FDF4 100%);
                border: 2px solid #86EFAC;
                border-radius: 18px;
                padding: 1.4rem;
                text-align: center;
                box-shadow: 0 6px 20px rgba(34, 197, 94, 0.12);
            ">
                <div style="font-family: 'Poppins', sans-serif; font-size: 0.82rem; font-weight: 700; color: #166534; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;">
                    TOTAL WISHLIST VALUE
                </div>
                <div style="font-family: 'Poppins', sans-serif; font-size: 2.3rem; font-weight: 800; color: #15803D; line-height: 1.1;">
                    {CURRENCY}{final_payable:,.2f}
                </div>
                <div style="font-size: 0.78rem; color: #166534; margin-top: 4px; font-weight: 600;">
                    ❤️ Saved items ready for express checkout
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # Actions Row
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])

    with btn_col1:
        if st.button("← Continue Shopping", key="wish_continue_bottom", use_container_width=True):
            go_to("home")
            st.rerun()

    with btn_col2:
        if st.button("🛒 Move All to Cart", key="wish_move_all", type="primary", use_container_width=True):
            for item in items:
                p = item["product"]
                q = item.get("qty", 1)
                v = item.get("variant", "1kg")
                add_to_cart(p, variant=v, qty=q)
            clear_wishlist()
            st.toast("Moved all wishlist items to Cart! 🎉")
            st.rerun()

    with btn_col3:
        if st.button("🗑️ Clear Wishlist", key="wish_clear_all", use_container_width=True):
            clear_wishlist()
            st.toast("Cleared wishlist")
            st.rerun()
