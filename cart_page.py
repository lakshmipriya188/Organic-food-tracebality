
"""Shopping cart page: line items, quantity editing and order summary."""

import streamlit as st
from config import CURRENCY
from utils.cart_manager import (
    cart_items, update_qty, remove_from_cart, cart_total, go_to
)


def render_cart_page():
    if st.button("← Continue shopping"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="om-section-title">Your Cart</div>', unsafe_allow_html=True)

    items = cart_items()
    if not items:
        st.info("Your cart is empty. Explore our millets, staples and more from the home page!")
        return

    col_items, col_summary = st.columns([2.2, 1])

    with col_items:
        for item in items:
            product = item["product"]
            c_img, c_info, c_qty, c_remove = st.columns([1, 3, 1.4, 0.8])
            with c_img:
                st.image(product.image_path, use_container_width=True)
            with c_info:
                st.markdown(f"**{product.name}**")
                st.caption(f"Variant: {item['variant']}")
                st.markdown(f"{CURRENCY} {product.price:,.2f} per unit")
            with c_qty:
                new_qty = st.number_input(
                    "qty", min_value=0, max_value=99, value=item["qty"],
                    key=f"qty_{item['key']}", label_visibility="collapsed"
                )
                if new_qty != item["qty"]:
                    update_qty(item["key"], new_qty)
                    st.rerun()
            with c_remove:
                if st.button("✕", key=f"rm_{item['key']}"):
                    remove_from_cart(item["key"])
                    st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

    with col_summary:
        st.markdown('<div class="om-product-card">', unsafe_allow_html=True)
        st.markdown("#### Order Summary")
        subtotal = cart_total(use_coop_price=False)
        coop_total = cart_total(use_coop_price=True)
        st.write(f"Subtotal: **{CURRENCY} {subtotal:,.2f}**")
        st.write(f"Co-Op member price: **{CURRENCY} {coop_total:,.2f}**")
        st.caption(f"You save {CURRENCY} {subtotal - coop_total:,.2f} as a Co-Op member.")
        st.write("Delivery: **Free**")
        st.markdown("---")
        st.markdown(f"### Total: {CURRENCY} {subtotal:,.2f}")
        if st.button("Proceed to Checkout", use_container_width=True):
            st.success("This is a demo storefront — checkout isn't wired to real payments yet.")
        st.markdown('</div>', unsafe_allow_html=True)

