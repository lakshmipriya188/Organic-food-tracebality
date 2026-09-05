"""
Streamlit Interactive Product Recommendation Engine
File: predication.py

Features:
- Inputs: 20 SHAP Selected Features
- Model Selection: LightGBM, XGBoost, Random Forest
- Recommends 1 product at a time (starting from Top 1)
- Detailed Session Activity Log & Shopping Summary above:
    * Cart Item Details: Original Price, Discount %, Price after Discount.
    * Cart Totals: Total Price without discount, Discount Savings, Final Payable Amount.
    * Wishlist Favorites with impressive prompt ("Still considering my suggestions?") and "Add to Cart 🛒" buttons.
    * Rejected items section with re-consideration prompt and "Move to Cart / Move to Wishlist" buttons.
- Rejection Apology & Next Product Recommendation.
- Acceptance Actions: 🛒 Add to Cart, ❤️ Add to Wishlist.
"""

import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# 20 SHAP-selected optimal features
selected_features = [
    'min_pp', 'p90_pp', 'p95_pad', 'p25_pp', 'p95_pp', 'max_pp',
    'min_pad', 'p75_pp', 'max_pad', 'p90_pad', 'avg_pp', 'p50_pp',
    'p25_pad', 'p50_pad', 'avg_pad', 'p75_pad', 'p90_pd', 'total_pad',
    'max_pd', 'p95_pd'
]

target_col = 'product_id'


@st.cache_resource
def load_assets():
    """Load trained models, label encoder, and products metadata."""
    models = {}
    model_files = {
        'LightGBM': ['lgbm_multiclass_model.pkl', 'lgbm_model.pkl'],
        'XGBoost': ['xgb_multiclass_model.pkl', 'xgb_model.pkl'],
        'Random Forest': ['rf_multiclass_model.pkl', 'rf_model.pkl']
    }

    for name, f_list in model_files.items():
        for fname in f_list:
            if os.path.exists(fname):
                try:
                    with open(fname, 'rb') as f:
                        models[name] = pickle.load(f)
                    break
                except Exception as e:
                    print(f"Could not load {fname}: {e}")

    encoder = None
    if os.path.exists('label_encoder.pkl'):
        try:
            with open('label_encoder.pkl', 'rb') as f:
                encoder = pickle.load(f)
        except Exception as e:
            print(f"Error loading label_encoder.pkl: {e}")

    products_df = None
    if os.path.exists('products.csv'):
        try:
            products_df = pd.read_csv('products.csv')
        except Exception:
            pass

    return models, encoder, products_df


def get_product_info(product_id, products_df):
    """Retrieve product details including price, discount, and final price."""
    if products_df is not None and 'product_id' in products_df.columns:
        match = products_df[products_df['product_id'] == product_id]
        if not match.empty:
            row = match.iloc[0]
            name = row.get('product_name', f'Product #{product_id}')
            price = float(row.get('price', 0.0))
            discount = float(row.get('discount', 10.0))  # Default 10% if missing
            price_after_disc = round(price * (1.0 - (discount / 100.0)), 2)
            category = row.get('category_name', row.get('category_id', 'N/A'))
            return name, price, discount, price_after_disc, category
    return f"Product #{product_id}", 0.0, 10.0, 0.0, "N/A"


def get_all_ranked_predictions(model, encoder, products_df, input_df):
    """Get all predictions ranked by probability."""
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


def main():
    st.set_page_config(
        page_title="Organic Product Recommendation Engine",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # CSS to hide Streamlit automatic sidebar navigation
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page Header
    st.title("📦 Organic Product Recommendation Engine")
    st.markdown("Enter the 20 SHAP Feature values below and select a machine learning model to get tailored product recommendations.")
    st.markdown("---")

    models, encoder, products_df = load_assets()

    if not models:
        st.error("⚠️ No trained model files found (`lgbm_multiclass_model.pkl`, `xgb_multiclass_model.pkl`, `rf_multiclass_model.pkl`).")
        return

    if encoder is None:
        st.error("⚠️ `label_encoder.pkl` file not found.")
        return

    # Initialize Session States
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

    # Model Selector
    model_choice = st.selectbox(
        "Select Prediction Model:",
        options=list(models.keys()),
        index=0
    )

    st.markdown("### Feature Inputs")

    # 20 Feature Inputs arranged in 4 Columns
    input_values = {}
    cols = st.columns(4)
    for idx, feature in enumerate(selected_features):
        col = cols[idx % 4]
        with col:
            input_values[feature] = st.number_input(
                f"{feature}:",
                value=10.0,
                key=f"input_{feature}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Trigger New Recommendation Session
    if st.button("🔮 Get Product Suggestion", use_container_width=True):
        st.session_state.has_run_prediction = True
        st.session_state.rejected_product_ids = set()
        st.session_state.accepted_product_ids = set()
        st.session_state.accepted_history = []
        st.session_state.rejected_history = []
        st.session_state.user_accepted_current = False
        st.session_state.last_action_msg = ""
        st.session_state.last_rejection_msg = ""

    if st.session_state.get("has_run_prediction", False):
        input_df = pd.DataFrame([input_values])[selected_features]
        m_obj = models[model_choice]

        # Fetch ranked predictions
        all_predictions = get_all_ranked_predictions(m_obj, encoder, products_df, input_df)

        # Filter out rejected & accepted products
        available_predictions = [
            p for p in all_predictions
            if p['product_id'] not in st.session_state.rejected_product_ids
            and p['product_id'] not in st.session_state.accepted_product_ids
        ]

        st.markdown("---")

        # Session Activity Log & Price Summary Shown Above
        if st.session_state.accepted_history or st.session_state.rejected_history:
            st.markdown("## 📊 Session Activity Summary & Cart Breakdown")
            
            cart_items = [x for x in st.session_state.accepted_history if x["action"] == "Cart"]
            wishlist_items = [x for x in st.session_state.accepted_history if x["action"] == "Wishlist"]
            rejected_items = st.session_state.rejected_history

            if cart_items:
                total_original = sum(x["price"] for x in cart_items)
                total_final = sum(x["final_price"] for x in cart_items)
                total_savings = total_original - total_final

                st.markdown("### 🛒 Cart Items & Price Breakdown")
                c_m1, c_m2, c_m3 = st.columns(3)
                c_m1.metric("Total Original Price (Without Discount)", f"₹{total_original:,.2f}")
                c_m2.metric("Total Discount Savings", f"₹{total_savings:,.2f}")
                c_m3.metric("Final Payable Amount", f"₹{total_final:,.2f}")

                for item in cart_items:
                    st.markdown(
                        f"- 🛒 **{item['name']}** (`#{item['id']}`) — Price: ~~₹{item['price']:,.2f}~~ | **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)"
                    )
                st.markdown("---")

            if wishlist_items:
                st.markdown("### ❤️ Wishlist Favorites")
                #st.info("✨ *Still considering my suggestions? You've saved these handpicked organic favorites in your Wishlist — move them to your Cart anytime you're ready!*")
                st.info("✨ *Not sure yet? Pop it in your Wishlist — no rush, it'll be waiting for you!*")
                
                for item in wishlist_items:
                    w_col1, w_col2 = st.columns([3.5, 1])
                    with w_col1:
                        st.markdown(
                            f"- ❤️ **{item['name']}** (`#{item['id']}`) — Price: ~~₹{item['price']:,.2f}~~ | **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)"
                        )
                    with w_col2:
                        if st.button("Add to Cart 🛒", key=f"wish_to_cart_{item['id']}"):
                            item["action"] = "Cart"
                            st.session_state.last_action_msg = f"🎉 Moved **{item['name']}** from Wishlist to **Cart**!"
                            st.rerun()
                st.markdown("---")

            if rejected_items:
                st.markdown("### 🔴 Rejected Recommendations")
                st.info("💡 *I may have guessed incorrectly earlier, but take another look — you can still move any rejected product directly to Cart or Wishlist!*")
                
                for item in rejected_items:
                    col_text, col_b1, col_b2 = st.columns([3, 1, 1])
                    with col_text:
                        st.markdown(f"- ❌ **{item['name']}** (`#{item['id']}`) — Price: **₹{item['final_price']:,.2f}** ({item['discount']:.0f}% OFF)")
                    with col_b1:
                        if st.button("Move to Cart 🛒", key=f"move_cart_{item['id']}"):
                            st.session_state.rejected_history = [x for x in st.session_state.rejected_history if x["id"] != item["id"]]
                            st.session_state.rejected_product_ids.discard(item["id"])
                            item_copy = item.copy()
                            item_copy["action"] = "Cart"
                            st.session_state.accepted_history.append(item_copy)
                            st.session_state.accepted_product_ids.add(item["id"])
                            st.session_state.last_action_msg = f"🎉 Moved **{item['name']}** from Rejected list to **Cart**!"
                            st.rerun()
                    with col_b2:
                        if st.button("Move to Wishlist ❤️", key=f"move_wish_{item['id']}"):
                            st.session_state.rejected_history = [x for x in st.session_state.rejected_history if x["id"] != item["id"]]
                            st.session_state.rejected_product_ids.discard(item["id"])
                            item_copy = item.copy()
                            item_copy["action"] = "Wishlist"
                            st.session_state.accepted_history.append(item_copy)
                            st.session_state.accepted_product_ids.add(item["id"])
                            st.session_state.last_action_msg = f"🎉 Moved **{item['name']}** from Rejected list to **Wishlist**!"
                            st.rerun()

            st.markdown("---")

        # Feedback messages
        if st.session_state.last_rejection_msg:
            st.warning(st.session_state.last_rejection_msg)

        if st.session_state.last_action_msg:
            st.success(st.session_state.last_action_msg)

        if not available_predictions:
            st.info("ℹ️ No more product suggestions available for these feature inputs! Enter new feature values above to start fresh.")
            return

        current_item = available_predictions[0]
        prod_id = current_item['product_id']

        st.markdown(f"### 🎯 Recommended Product (Model: {model_choice})")

        with st.container():
            col_info, col_actions = st.columns([3, 2])

            with col_info:
                st.markdown(f"### {current_item['product_name']}")
                st.markdown(f"**Model Rank:** #{current_item['rank']} | **Product ID:** `#{prod_id}`")
                st.markdown(f"**Original Price:** ~~₹{current_item['price']:,.2f}~~ | **Final Price:** **₹{current_item['final_price']:,.2f}** ({current_item['discount']:.0f}% OFF)")
                st.markdown(f"**Category:** {current_item['category']}")
                st.markdown(f"**Model Confidence Score:** `{current_item['probability']:.2f}%`")
                st.progress(float(current_item['raw_prob']))

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
                        st.session_state.last_rejection_msg = "😔 I am sorry for suggesting a bad one! Can you please allow me to suggest a product for the next one..."
                        st.session_state.last_action_msg = ""
                        st.session_state.user_accepted_current = False
                        st.rerun()

                else:
                    st.success("✅ **Product Accepted! Choose an action below:**")
                    
                    b_cart = st.button("🛒 Add to Cart", key=f"cart_{prod_id}", use_container_width=True)
                    b_wish = st.button("❤️ Add to Wishlist", key=f"wish_{prod_id}", use_container_width=True)

                    if b_cart:
                        st.session_state.accepted_product_ids.add(prod_id)
                        st.session_state.accepted_history.append({
                            "id": prod_id,
                            "name": current_item['product_name'],
                            "price": current_item['price'],
                            "discount": current_item['discount'],
                            "final_price": current_item['final_price'],
                            "action": "Cart"
                        })
                        st.session_state.last_action_msg = f"🎉 **{current_item['product_name']}** added to your **Cart** successfully!"
                        st.session_state.user_accepted_current = False
                        st.session_state.last_rejection_msg = ""
                        st.rerun()

                    if b_wish:
                        st.session_state.accepted_product_ids.add(prod_id)
                        st.session_state.accepted_history.append({
                            "id": prod_id,
                            "name": current_item['product_name'],
                            "price": current_item['price'],
                            "discount": current_item['discount'],
                            "final_price": current_item['final_price'],
                            "action": "Wishlist"
                        })
                        st.session_state.last_action_msg = f"🎉 **{current_item['product_name']}** added to your **Wishlist** successfully!"
                        st.session_state.user_accepted_current = False
                        st.session_state.last_rejection_msg = ""
                        st.rerun()


if __name__ == '__main__':
    main()
