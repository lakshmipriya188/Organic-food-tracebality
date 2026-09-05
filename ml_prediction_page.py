"""
Streamlit UI for AI Product Recommendation Engine (LightGBM)
Integrates logged-in customer ID, extracts 20 SHAP features from Order_Details database,
and syncs Add to Cart / Add to Wishlist actions directly with main application UI.
"""

import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import mysql.connector
from mysql.connector import Error

from utils.cart_manager import go_to, add_to_cart, toggle_wishlist
from products import get_product_by_id
from utils.image_utils import get_image_src

SELECTED_FEATURES = [
    'min_pp', 'p90_pp', 'p95_pad', 'p25_pp', 'p95_pp', 'max_pp',
    'min_pad', 'p75_pp', 'max_pad', 'p90_pad', 'avg_pp', 'p50_pp',
    'p25_pad', 'p50_pad', 'avg_pad', 'p75_pad', 'p90_pd', 'total_pad',
    'max_pd', 'p95_pd'
]

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root123")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "farmora")


def get_direct_db_connection():
    """Establish direct connection to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            autocommit=True
        )
        return conn
    except Error:
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database="organic_food_traceability",
                autocommit=True
            )
            return conn
        except Error:
            return None


def fetch_customer_info_and_features(customer_id: int):
    """
    Directly queries database for Customer_Details & Order_Details by customer_id.
    Returns (cust_info_dict, features_df, error_msg).
    """
    FALLBACK_CUSTOMERS = [
        {"customer_id": 1, "customer_name": "Rahul Sharma", "email_id": "rahul@gmail.com"},
        {"customer_id": 2, "customer_name": "Priya Singh", "email_id": "priya@gmail.com"},
        {"customer_id": 3, "customer_name": "Amit Kumar", "email_id": "amit@gmail.com"},
        {"customer_id": 4, "customer_name": "Sneha Reddy", "email_id": "sneha@gmail.com"},
        {"customer_id": 5, "customer_name": "Arjun Patel", "email_id": "arjun@gmail.com"},
    ]

    conn = get_direct_db_connection()
    cust_info = None
    orders = []

    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT customer_id, customer_name, email_id FROM Customer_Details WHERE customer_id = %s;",
                (int(customer_id),)
            )
            cust_info = cursor.fetchone()

            if cust_info:
                cursor.execute(
                    """SELECT product_price, product_discount, price_after_discount 
                       FROM Order_Details WHERE customer_id = %s;""",
                    (int(customer_id),)
                )
                orders = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"DB query notice: {e}")

    # Fallback in-memory check
    if not cust_info:
        for fc in FALLBACK_CUSTOMERS:
            if fc["customer_id"] == int(customer_id):
                cust_info = fc
                orders = [
                    {"product_price": 180.0, "product_discount": 10.0, "price_after_discount": 162.0},
                    {"product_price": 350.0, "product_discount": 12.0, "price_after_discount": 308.0},
                    {"product_price": 95.0, "product_discount": 14.0, "price_after_discount": 81.70},
                    {"product_price": 1450.0, "product_discount": 9.0, "price_after_discount": 1319.50},
                ]
                break

    if not cust_info or not orders:
        return None, None, "Customer is not in the current database"

    df_orders = pd.DataFrame(orders)
    pp = df_orders['product_price'].astype(float).values
    pd_disc = df_orders['product_discount'].astype(float).values
    pad = df_orders['price_after_discount'].astype(float).values

    feature_dict = {
        'min_pp': float(np.min(pp)),
        'p90_pp': float(np.percentile(pp, 90)),
        'p95_pad': float(np.percentile(pad, 95)),
        'p25_pp': float(np.percentile(pp, 25)),
        'p95_pp': float(np.percentile(pp, 95)),
        'max_pp': float(np.max(pp)),
        'min_pad': float(np.min(pad)),
        'p75_pp': float(np.percentile(pp, 75)),
        'max_pad': float(np.max(pad)),
        'p90_pad': float(np.percentile(pad, 90)),
        'avg_pp': float(np.mean(pp)),
        'p50_pp': float(np.percentile(pp, 50)),
        'p25_pad': float(np.percentile(pad, 25)),
        'p50_pad': float(np.percentile(pad, 50)),
        'avg_pad': float(np.mean(pad)),
        'p75_pad': float(np.percentile(pad, 75)),
        'p90_pd': float(np.percentile(pd_disc, 90)),
        'total_pad': float(np.sum(pad)),
        'max_pd': float(np.max(pd_disc)),
        'p95_pd': float(np.percentile(pd_disc, 95))
    }

    features_df = pd.DataFrame([feature_dict])[SELECTED_FEATURES]
    return cust_info, features_df, None


@st.cache_resource
def load_ml_assets():
    """Load LightGBM model, label encoder, and products metadata using robust multi-path resolution."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()

    def resolve_path(fname):
        candidates = [
            os.path.join(base_dir, fname),
            os.path.join(cwd, fname),
            fname,
            os.path.abspath(fname)
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    model = None
    model_files = ['lgbm_multiclass_model.pkl', 'lgbm_model.pkl', 'xgb_multiclass_model.pkl', 'rf_multiclass_model.pkl']

    for fname in model_files:
        resolved_p = resolve_path(fname)
        if resolved_p:
            try:
                with open(resolved_p, 'rb') as f:
                    model = pickle.load(f)
                break
            except Exception as e:
                print(f"Could not load {resolved_p}: {e}")

    encoder = None
    enc_path = resolve_path('label_encoder.pkl')
    if enc_path:
        try:
            with open(enc_path, 'rb') as f:
                encoder = pickle.load(f)
        except Exception as e:
            print(f"Error loading label_encoder.pkl: {e}")

    products_df = None
    prod_csv_path = resolve_path('products.csv')
    if prod_csv_path:
        try:
            products_df = pd.read_csv(prod_csv_path)
        except Exception:
            pass

    return model, encoder, products_df


def get_product_info(product_id, products_df):
    """Lookup product metadata."""
    if products_df is not None and 'product_id' in products_df.columns:
        match = products_df[products_df['product_id'] == product_id]
        if not match.empty:
            row = match.iloc[0]
            name = row.get('product_name', f'Product #{product_id}')
            price = float(row.get('price', 0.0))
            discount = float(row.get('discount', 10.0))
            price_after_disc = round(price * (1.0 - (discount / 100.0)), 2)
            category = row.get('category_name', row.get('category_id', 'N/A'))
            return name, price, discount, price_after_disc, category
    return f"Product #{product_id}", 0.0, 10.0, 0.0, "N/A"


def get_all_ranked_predictions(model, encoder, products_df, input_df):
    """Rank all products by probability."""
    probs = model.predict_proba(input_df)[0]
    sorted_indices = np.argsort(probs)[::-1]

    results = []
    for rank, idx in enumerate(sorted_indices, 1):
        prob_pct = probs[idx] * 100.0
        prod_id = int(encoder.inverse_transform([idx])[0]) if encoder else int(idx)
        p_name, p_price, p_disc, p_final_price, p_cat = get_product_info(prod_id, products_df)
        results.append({
            'rank': rank,
            'product_id': prod_id,
            'product_name': p_name,
            'price': p_price,
            'discount': p_disc,
            'final_price': p_final_price,
            'category': p_cat,
            'probability': prob_pct,
            'raw_prob': probs[idx]
        })
    return results


def render_ml_prediction_page():
    # Top action bar
    top_col1, _ = st.columns([1.5, 4])
    with top_col1:
        if st.button("← Back to Main Store UI", key="pred_back_top", use_container_width=True):
            go_to("home")
            st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-top:0.8rem; margin-bottom:4px;">
            AI ORGANIC RECOMMENDATION ENGINE
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:1.5rem;">
            🤖 Personalized Product Prediction Portal
        </div>
        """,
        unsafe_allow_html=True
    )

    model, encoder, products_df = load_ml_assets()

    if not model or encoder is None:
        st.error("⚠️ LightGBM model or Label Encoder could not be loaded. Please verify pickle files.")
        return

    # Always use current logged-in customer
    active_cid = st.session_state.get("user_id") or 1
    current_uname = st.session_state.get("user") or "Customer"

    # Reset activity breakdown state on new user login / session refresh
    if st.session_state.get("last_pred_user_id") != active_cid:
        st.session_state.last_pred_user_id = active_cid
        st.session_state.rejected_product_ids = set()
        st.session_state.accepted_product_ids = set()
        st.session_state.accepted_history = []
        st.session_state.rejected_history = []
        st.session_state.user_accepted_current = False
        st.session_state.last_action_msg = ""
        st.session_state.last_rejection_msg = ""

    # Ensure Session State Initialization
    if "rejected_product_ids" not in st.session_state:
        st.session_state.rejected_product_ids = set()
    if "accepted_product_ids" not in st.session_state:
        st.session_state.accepted_product_ids = set()
    if "accepted_history" not in st.session_state:
        st.session_state.accepted_history = []
    if "rejected_history" not in st.session_state:
        st.session_state.rejected_history = []
    if "user_accepted_current" not in st.session_state:
        st.session_state.user_accepted_current = False
    if "last_action_msg" not in st.session_state:
        st.session_state.last_action_msg = ""
    if "last_rejection_msg" not in st.session_state:
        st.session_state.last_rejection_msg = ""

    # Fetch Customer Info & Features from Database
    cust_info, feat_df, err = fetch_customer_info_and_features(active_cid)

    if err or feat_df is None:
        st.error("Customer is not in the current database")
        return

    # Display Customer Profile Card (Customer Name only)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1B4D3E 0%, #0F291E 100%);
            border-radius: 18px;
            padding: 1.4rem 1.8rem;
            color: #FFFFFF;
            margin: 0.5rem 0 1.5rem 0;
            box-shadow: 0 8px 24px rgba(27, 77, 62, 0.15);
        ">
            <div style="font-size: 0.78rem; font-weight: 800; color: #4ADE80; letter-spacing: 1.5px; text-transform: uppercase;">
                VERIFIED CUSTOMER PROFILE
            </div>
            <div style="font-size: 1.9rem; font-weight: 800; font-family: 'Poppins', sans-serif; color: #FFFFFF; margin: 4px 0 2px 0;">
                👤 Customer Name: {cust_info.get('customer_name', current_uname)}
            </div>
            <div style="font-size: 0.92rem; color: #DCFCE7;">
                📧 Email ID: <b>{cust_info.get('email_id', 'N/A')}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate predictions using LightGBM
    all_predictions = get_all_ranked_predictions(model, encoder, products_df, feat_df)

    # Filter out rejected & accepted products
    available_predictions = [
        p for p in all_predictions
        if p['product_id'] not in st.session_state.rejected_product_ids
        and p['product_id'] not in st.session_state.accepted_product_ids
    ]

    # Feedback messages
    if st.session_state.last_rejection_msg:
        st.warning(st.session_state.last_rejection_msg)

    if st.session_state.last_action_msg:
        st.success(st.session_state.last_action_msg)

    if not available_predictions:
        st.info("ℹ️ No more recommendations available.")
        return

    current_item = available_predictions[0]
    prod_id = current_item['product_id']

    st.markdown("### 🎯 Recommended Product")

    with st.container():
        col_info, col_actions = st.columns([3, 2])

        with col_info:
            st.markdown(f"### {current_item['product_name']}")
            st.markdown(f"**Original Price:** ~~₹{current_item['price']:,.2f}~~ | **Final Price:** **₹{current_item['final_price']:,.2f}** ({current_item['discount']:.0f}% OFF)")

        with col_actions:
            st.write("")
            st.write("")
            if not st.session_state.user_accepted_current:
                st.markdown("**Do you like this product suggestion?**")
                c_acc, c_rej = st.columns(2)
                
                if c_acc.button("Accept ✅", key=f"btn_accept_{prod_id}"):
                    st.session_state.user_accepted_current = True
                    st.session_state.last_rejection_msg = ""
                    st.rerun()

                if c_rej.button("Reject ❌", key=f"btn_reject_{prod_id}"):
                    st.session_state.rejected_product_ids.add(prod_id)
                    st.session_state.rejected_history.append({
                        "id": prod_id,
                        "name": current_item['product_name'],
                        "price": current_item['price'],
                        "discount": current_item['discount'],
                        "final_price": current_item['final_price']
                    })
                    st.session_state.last_rejection_msg = "😔 Sorry for suggesting a bad one! Loading next recommendation..."
                    st.session_state.last_action_msg = ""
                    st.session_state.user_accepted_current = False
                    st.rerun()

            else:
                st.success("✅ **Product Accepted! Choose an action:**")
                
                b_cart = st.button("🛒 Add to Cart", key=f"cart_{prod_id}", use_container_width=True)
                b_wish = st.button("❤️ Add to Wishlist", key=f"wish_{prod_id}", use_container_width=True)

                # SYNC WITH MAIN APP CART & WISHLIST
                prod_dataclass = get_product_by_id(str(prod_id))

                if b_cart:
                    st.session_state.accepted_product_ids.add(prod_id)
                    if prod_dataclass:
                        add_to_cart(prod_dataclass, variant="1kg", qty=1)
                    
                    st.session_state.accepted_history.append({
                        "id": prod_id,
                        "name": current_item['product_name'],
                        "price": current_item['price'],
                        "discount": current_item['discount'],
                        "final_price": current_item['final_price'],
                        "action": "Cart"
                    })
                    st.session_state.last_action_msg = f"🎉 **{current_item['product_name']}** added to Cart!"
                    st.session_state.user_accepted_current = False
                    st.session_state.last_rejection_msg = ""
                    st.rerun()

                if b_wish:
                    st.session_state.accepted_product_ids.add(prod_id)
                    if prod_dataclass:
                        toggle_wishlist(prod_dataclass)
                    
                    st.session_state.accepted_history.append({
                        "id": prod_id,
                        "name": current_item['product_name'],
                        "price": current_item['price'],
                        "discount": current_item['discount'],
                        "final_price": current_item['final_price'],
                        "action": "Wishlist"
                    })
                    st.session_state.last_action_msg = f"🎉 **{current_item['product_name']}** added to Wishlist!"
                    st.session_state.user_accepted_current = False
                    st.session_state.last_rejection_msg = ""
                    st.rerun()

    # Session Activity Breakdown
    if st.session_state.accepted_history or st.session_state.rejected_history:
        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin: 2rem 0 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("### 📊 AI Session Activity Breakdown")

        cart_items_list = [x for x in st.session_state.accepted_history if x["action"] == "Cart"]
        wishlist_items_list = [x for x in st.session_state.accepted_history if x["action"] == "Wishlist"]
        rejected_items_list = st.session_state.rejected_history

        if cart_items_list:
            st.markdown("#### 🛒 Items Synced to Main Shopping Cart")
            for item in cart_items_list:
                st.markdown(f"- 🛒 **{item['name']}** — Price: ~~₹{item['price']:,.2f}~~ | **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)")
            
        if wishlist_items_list:
            st.markdown("#### ❤️ Items Synced to Main Wishlist")
            for item in wishlist_items_list:
                st.markdown(f"- ❤️ **{item['name']}** — Price: ~~₹{item['price']:,.2f}~~ | **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)")

        if rejected_items_list:
            st.markdown("#### 🔴 Rejected Recommendations")
            for item in rejected_items_list:
                st.markdown(f"- ❌ **{item['name']}** — Price: **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Continue Shopping in Main UI", key="pred_back_bottom", use_container_width=True):
        go_to("home")
        st.rerun()


if __name__ == '__main__':
    render_ml_prediction_page()
