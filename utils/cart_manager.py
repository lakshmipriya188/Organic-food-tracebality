"""Cart, Wishlist, Pincode Locator, and Navigation Session Manager."""

import streamlit as st
from typing import Any
from config import DEFAULT_PINCODE
from db_manager import (
    add_or_update_cart_db, update_cart_count_db, remove_from_cart_db,
    clear_cart_db, fetch_cart_items_db
)

# In-memory per-user cart fallback storage
FALLBACK_USER_CARTS = {}


def _init_state():
    """Ensure all required session state keys exist and manage per-user cart loading."""
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
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "current_cart_user_id" not in st.session_state:
        st.session_state.current_cart_user_id = None

    # Enforce cart user scoping
    current_uid = st.session_state.user_id
    if current_uid is None:
        if st.session_state.cart:
            st.session_state.cart = {}
        if st.session_state.wishlist:
            st.session_state.wishlist = {}
        st.session_state.current_cart_user_id = None
    elif st.session_state.current_cart_user_id != current_uid:
        load_cart_from_db(current_uid)


def load_cart_from_db(user_id: int):
    """Load user's cart from MySQL Cart table (or in-memory store) into session state."""
    st.session_state.cart = {}
    st.session_state.current_cart_user_id = user_id

    if not user_id:
        return

    from products import get_product_by_id

    loaded_from_db = False
    try:
        db_items = fetch_cart_items_db(int(user_id))
        if db_items:
            for row in db_items:
                prod = get_product_by_id(str(row["product_id"]))
                if prod:
                    key = f"{prod.id}_1kg"
                    st.session_state.cart[key] = {
                        "key": key,
                        "product": prod,
                        "variant": "1kg",
                        "qty": row["product_count"]
                    }
            loaded_from_db = True
    except Exception as e:
        print(f"Error loading cart from DB: {e}")

    if loaded_from_db:
        FALLBACK_USER_CARTS[int(user_id)] = dict(st.session_state.cart)
    else:
        # Check fallback storage if DB returned no rows or was offline
        fallback_cart = FALLBACK_USER_CARTS.get(int(user_id), {})
        st.session_state.cart = dict(fallback_cart)


def logout_user():
    """Clear session state user and cart data on logout."""
    _init_state()
    st.session_state.user = None
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.session_state.cart = {}
    st.session_state.wishlist = {}
    st.session_state.current_cart_user_id = None
    st.session_state.page = "login"


def sync_cart_state():
    """Backup current user's cart to fallback dictionary."""
    user_id = st.session_state.get("user_id")
    if user_id:
        FALLBACK_USER_CARTS[int(user_id)] = dict(st.session_state.get("cart", {}))


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
    """Add product item to cart in session state and MySQL Cart table."""
    _init_state()
    user_id = st.session_state.get("user_id")
    if not user_id:
        return

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
    
    sync_cart_state()

    # Sync with MySQL DB
    try:
        pid = int(product.id)
        mrp = float(product.original_price) if getattr(product, 'original_price', None) and product.original_price > product.price else float(product.price)
        disc = float(getattr(product, 'discount_pct', 0.0) or 0.0)
        add_or_update_cart_db(customer_id=int(user_id), product_id=pid, count=qty, price=mrp, discount=disc)
    except Exception as e:
        print(f"Cart DB Sync note: {e}")


def remove_from_cart(item_key: str, product_id: Any = None):
    """Remove item from cart by key and update DB."""
    _init_state()
    user_id = st.session_state.get("user_id")
    if item_key in st.session_state.cart:
        if product_id is None:
            product_id = st.session_state.cart[item_key]["product"].id
        del st.session_state.cart[item_key]

    sync_cart_state()

    if user_id and product_id is not None:
        try:
            remove_from_cart_db(customer_id=int(user_id), product_id=int(product_id))
        except Exception as e:
            print(f"Cart DB remove note: {e}")


def update_qty(item_key: str, qty: int, product_id: Any = None):
    """Update item quantity in cart and DB."""
    _init_state()
    user_id = st.session_state.get("user_id")
    if item_key in st.session_state.cart:
        if product_id is None:
            product_id = st.session_state.cart[item_key]["product"].id
        if qty <= 0:
            del st.session_state.cart[item_key]
        else:
            st.session_state.cart[item_key]["qty"] = qty

    sync_cart_state()

    if user_id and product_id is not None:
        try:
            update_cart_count_db(customer_id=int(user_id), product_id=int(product_id), new_count=qty)
        except Exception as e:
            print(f"Cart DB update note: {e}")


def cart_items():
    """Return list of cart item dicts."""
    _init_state()
    return list(st.session_state.cart.values())


def cart_total() -> float:
    """Calculate total final price of cart."""
    _init_state()
    total = 0.0
    for item in st.session_state.cart.values():
        p = item["product"]
        total += p.price * item["qty"]
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
