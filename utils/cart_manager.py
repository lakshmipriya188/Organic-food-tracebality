"""Cart, Wishlist, Pincode Locator, and Navigation Session Manager."""

import streamlit as st
from typing import Any
from config import DEFAULT_PINCODE
from db_manager import (
    add_or_update_cart_db, update_cart_count_db, remove_from_cart_db,
    clear_cart_db, fetch_cart_items_db,
    add_or_update_wishlist_db, update_wishlist_count_db, remove_from_wishlist_db,
    clear_wishlist_db, fetch_wishlist_items_db
)

# In-memory per-user fallback storage
FALLBACK_USER_CARTS = {}
FALLBACK_USER_WISHLISTS = {}


def _init_state():
    """Ensure all required session state keys exist and manage per-user cart/wishlist loading."""
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

    # Enforce cart & wishlist user scoping
    current_uid = st.session_state.user_id
    if current_uid is None:
        if st.session_state.cart:
            st.session_state.cart = {}
        if st.session_state.wishlist:
            st.session_state.wishlist = {}
        st.session_state.current_cart_user_id = None
    elif st.session_state.current_cart_user_id != current_uid:
        load_cart_from_db(current_uid)
        load_wishlist_from_db(current_uid)


def load_cart_from_db(user_id: int):
    """Load user's cart from MySQL Cart table (or in-memory store) into session state."""
    st.session_state.cart = {}
    st.session_state.current_cart_user_id = user_id

    if not user_id:
        return

    # Automatically load user's wishlist alongside cart
    load_wishlist_from_db(user_id)

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


def load_wishlist_from_db(user_id: int):
    """Load user's wishlist from MySQL Wishlist table (or in-memory store) into session state."""
    st.session_state.wishlist = {}

    if not user_id:
        return

    from products import get_product_by_id

    loaded_from_db = False
    try:
        db_items = fetch_wishlist_items_db(int(user_id))
        if db_items:
            for row in db_items:
                prod = get_product_by_id(str(row["product_id"]))
                if prod:
                    key = f"{prod.id}_1kg"
                    st.session_state.wishlist[key] = {
                        "key": key,
                        "product": prod,
                        "variant": "1kg",
                        "qty": row["product_count"]
                    }
            loaded_from_db = True
    except Exception as e:
        print(f"Error loading wishlist from DB: {e}")

    if loaded_from_db:
        FALLBACK_USER_WISHLISTS[int(user_id)] = dict(st.session_state.wishlist)
    else:
        fallback_wish = FALLBACK_USER_WISHLISTS.get(int(user_id), {})
        st.session_state.wishlist = dict(fallback_wish)


def logout_user():
    """Clear session state user, cart, and wishlist data on logout."""
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


def sync_wishlist_state():
    """Backup current user's wishlist to fallback dictionary."""
    user_id = st.session_state.get("user_id")
    if user_id:
        FALLBACK_USER_WISHLISTS[int(user_id)] = dict(st.session_state.get("wishlist", {}))


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


# --- CART FUNCTIONS ---

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


# --- WISHLIST FUNCTIONS (REPLICA OF CART) ---

def add_to_wishlist(product, variant: str = "1kg", qty: int = 1):
    """Add product item to wishlist in session state and MySQL Wishlist table."""
    _init_state()
    user_id = st.session_state.get("user_id")
    if not user_id:
        return

    key = f"{product.id}_{variant}"
    if key in st.session_state.wishlist:
        if isinstance(st.session_state.wishlist[key], dict):
            st.session_state.wishlist[key]["qty"] += qty
        else:
            st.session_state.wishlist[key] = {
                "key": key,
                "product": product,
                "variant": variant,
                "qty": qty + 1,
            }
    else:
        st.session_state.wishlist[key] = {
            "key": key,
            "product": product,
            "variant": variant,
            "qty": qty,
        }

    sync_wishlist_state()

    # Sync with MySQL DB
    try:
        pid = int(product.id)
        mrp = float(product.original_price) if getattr(product, 'original_price', None) and product.original_price > product.price else float(product.price)
        disc = float(getattr(product, 'discount_pct', 0.0) or 0.0)
        add_or_update_wishlist_db(customer_id=int(user_id), product_id=pid, count=qty, price=mrp, discount=disc)
    except Exception as e:
        print(f"Wishlist DB Sync note: {e}")


def remove_from_wishlist(item_key: str, product_id: Any = None):
    """Remove item from wishlist by key or product_id and update DB."""
    _init_state()
    user_id = st.session_state.get("user_id")
    pid = product_id

    # Check key matching or product_id matching
    keys_to_del = []
    for k, item in st.session_state.wishlist.items():
        if k == item_key:
            keys_to_del.append(k)
            if pid is None:
                pid = item["product"].id if isinstance(item, dict) else getattr(item, "id", None)
        elif str(k) == str(item_key) or (isinstance(item, dict) and str(item.get("product", {}).id) == str(item_key)) or (hasattr(item, "id") and str(item.id) == str(item_key)):
            keys_to_del.append(k)
            if pid is None:
                pid = item["product"].id if isinstance(item, dict) else getattr(item, "id", None)

    for k in keys_to_del:
        del st.session_state.wishlist[k]

    sync_wishlist_state()

    if user_id and pid is not None:
        try:
            remove_from_wishlist_db(customer_id=int(user_id), product_id=int(pid))
        except Exception as e:
            print(f"Wishlist DB remove note: {e}")


def update_wishlist_qty(item_key: str, qty: int, product_id: Any = None):
    """Update item quantity in wishlist and DB."""
    _init_state()
    user_id = st.session_state.get("user_id")
    if item_key in st.session_state.wishlist:
        if product_id is None and isinstance(st.session_state.wishlist[item_key], dict):
            product_id = st.session_state.wishlist[item_key]["product"].id
        if qty <= 0:
            del st.session_state.wishlist[item_key]
        else:
            if isinstance(st.session_state.wishlist[item_key], dict):
                st.session_state.wishlist[item_key]["qty"] = qty
            else:
                p = st.session_state.wishlist[item_key]
                st.session_state.wishlist[item_key] = {
                    "key": item_key,
                    "product": p,
                    "variant": "1kg",
                    "qty": qty
                }

    sync_wishlist_state()

    if user_id and product_id is not None:
        try:
            update_wishlist_count_db(customer_id=int(user_id), product_id=int(product_id), new_count=qty)
        except Exception as e:
            print(f"Wishlist DB update note: {e}")


def clear_wishlist(user_id: int = None):
    """Clear all items from customer's wishlist."""
    _init_state()
    uid = user_id or st.session_state.get("user_id")
    st.session_state.wishlist = {}
    sync_wishlist_state()
    if uid:
        try:
            clear_wishlist_db(int(uid))
        except Exception as e:
            print(f"Wishlist DB clear note: {e}")


def toggle_wishlist(product, variant: str = "1kg", qty: int = 1):
    """Toggle product in wishlist."""
    _init_state()
    if is_in_wishlist(product.id):
        remove_from_wishlist(str(product.id), product_id=product.id)
    else:
        add_to_wishlist(product, variant=variant, qty=qty)


def is_in_wishlist(product_id: Any) -> bool:
    """Check if product is in wishlist."""
    _init_state()
    pid = str(product_id)
    for k, item in st.session_state.wishlist.items():
        if str(k) == pid or str(k).startswith(f"{pid}_"):
            return True
        if isinstance(item, dict) and str(item.get("product", {}).id) == pid:
            return True
        if hasattr(item, "id") and str(item.id) == pid:
            return True
    return False


def wishlist_items():
    """Return list of wishlist item dicts (normalized to dict format)."""
    _init_state()
    res = []
    for k, item in st.session_state.wishlist.items():
        if isinstance(item, dict):
            res.append(item)
        else:
            # Handle legacy object in state if any
            res.append({
                "key": f"{item.id}_1kg",
                "product": item,
                "variant": "1kg",
                "qty": 1
            })
    return res


def wishlist_total() -> float:
    """Calculate total final price of wishlist."""
    _init_state()
    total = 0.0
    for item in wishlist_items():
        p = item["product"]
        total += p.price * item.get("qty", 1)
    return total


def wishlist_count() -> int:
    """Total items/quantity in wishlist."""
    _init_state()
    return sum(item.get("qty", 1) for item in wishlist_items())
