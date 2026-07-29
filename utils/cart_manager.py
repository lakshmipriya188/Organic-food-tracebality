"""Cart, Wishlist, Pincode Locator, and Navigation Session Manager."""

import streamlit as st
from config import DEFAULT_PINCODE


def _init_state():
    """Ensure all required session state keys exist."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "active_category" not in st.session_state:
        st.session_state.active_category = None
    if "fav_tab" not in st.session_state:
        st.session_state.fav_tab = "Bestsellers"
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "deliver_pincode" not in st.session_state:
        st.session_state.deliver_pincode = DEFAULT_PINCODE
    if "is_coop_member" not in st.session_state:
        st.session_state.is_coop_member = True
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = {}
    if "user" not in st.session_state:
        st.session_state.user = None


def go_to(page: str, active_category=None):
    """Navigate to a specified page."""
    _init_state()
    st.session_state.page = page
    if active_category is not None:
        st.session_state.active_category = active_category


def toggle_coop_member():
    """Toggle Co-Op Member pricing status."""
    _init_state()
    st.session_state.is_coop_member = not st.session_state.is_coop_member


def add_to_cart(product, variant: str = "1kg", qty: int = 1):
    """Add product item to cart."""
    _init_state()
    key = f"{product.id}_{variant}"
    if key in st.session_state.cart:
        st.session_state.cart[key]["qty"] += qty
    else:
        st.session_state.cart[key] = {
            "key": key,
            "product": product,
            "variant": variant,
            "qty": qty,
        }


def remove_from_cart(item_key: str):
    """Remove item from cart by key."""
    _init_state()
    if item_key in st.session_state.cart:
        del st.session_state.cart[item_key]


def update_qty(item_key: str, qty: int):
    """Update item quantity in cart."""
    _init_state()
    if item_key in st.session_state.cart:
        if qty <= 0:
            del st.session_state.cart[item_key]
        else:
            st.session_state.cart[item_key]["qty"] = qty


def cart_items():
    """Return list of cart item dicts."""
    _init_state()
    return list(st.session_state.cart.values())


def cart_total() -> float:
    """Calculate total price based on Co-Op membership."""
    _init_state()
    use_coop = st.session_state.is_coop_member
    total = 0.0
    for item in st.session_state.cart.values():
        p = item["product"]
        price = p.coop_price if (use_coop and p.coop_price > 0) else p.price
        total += price * item["qty"]
    return total


def cart_count() -> int:
    """Total items in cart."""
    _init_state()
    return sum(item["qty"] for item in st.session_state.cart.values())


def toggle_wishlist(product):
    """Toggle product in wishlist."""
    _init_state()
    if product.id in st.session_state.wishlist:
        del st.session_state.wishlist[product.id]
    else:
        st.session_state.wishlist[product.id] = product


def is_in_wishlist(product_id: str) -> bool:
    """Check if product is in wishlist."""
    _init_state()
    return product_id in st.session_state.wishlist


def wishlist_items():
    """Return list of wishlist product objects."""
    _init_state()
    return list(st.session_state.wishlist.values())


def remove_from_wishlist(product_id: str):
    """Remove product from wishlist."""
    _init_state()
    if product_id in st.session_state.wishlist:
        del st.session_state.wishlist[product_id]
