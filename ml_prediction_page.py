"""
Streamlit UI for LightGBM Forward & Reverse Product Classification
- Forward Prediction: 20 Features --> Predicted Product ID & Top 5 Probabilities
- Reverse Prediction: Selected Product ID --> Predicted Expected Feature Profile
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from utils.cart_manager import go_to
from utils.image_utils import get_image_src

SELECTED_FEATURES = [
    'min_pp', 'p90_pp', 'p95_pad', 'p25_pp', 'p95_pp', 'max_pp',
    'min_pad', 'p75_pp', 'max_pad', 'p90_pad', 'avg_pp', 'p50_pp',
    'p25_pad', 'p50_pad', 'avg_pad', 'p75_pad', 'p90_pd', 'total_pad',
    'max_pd', 'p95_pd'
]

@st.cache_resource
def load_ml_assets():
    """Load LightGBM model, label encoder, product catalog, and reverse profiles."""
    model_path = 'lgbm_multiclass_model.pkl'
    if not os.path.exists(model_path):
        model_path = 'lgbm_model.pkl'

    encoder_path = 'label_encoder.pkl'
    profiles_path = 'reverse_class_profiles.pkl'
    
    model = None
    encoder = None
    reverse_profiles = None
    products_df = None

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

    if os.path.exists(encoder_path):
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)

    if os.path.exists(profiles_path):
        with open(profiles_path, 'rb') as f:
            reverse_profiles = pickle.load(f)

    if os.path.exists('products.csv'):
        products_df = pd.read_csv('products.csv')

    return model, encoder, reverse_profiles, products_df


@st.cache_data
def load_sample_dataset():
    """Load sample preview of Final_Feature_code.csv for quick UI selection."""
    if os.path.exists('Final_Feature_code.csv'):
        cols = SELECTED_FEATURES + ['product_id']
        return pd.read_csv('Final_Feature_code.csv', nrows=2000, usecols=cols)
    return None


def get_product_details(prod_id, products_df):
    """Lookup product metadata from products.csv."""
    if products_df is not None and 'product_id' in products_df.columns:
        match = products_df[products_df['product_id'] == prod_id]
        if not match.empty:
            row = match.iloc[0]
            name = row.get('product_name', f'Product #{prod_id}')
            price = row.get('price', 0.0)
            category_id = row.get('category_id', 'N/A')
            return name, price, category_id
    return f"Product #{prod_id}", 0.0, "N/A"


def render_ml_prediction_page():
    if st.button("← Back to Home"):
        go_to("home")
        st.rerun()

    st.markdown(
        """
        <div style="font-family:'Poppins', sans-serif; font-size:0.82rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
            AI MODEL PREDICTION ENGINE
        </div>
        <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:700; color:#1B4D3E; margin-bottom:0.5rem;">
            🤖 LightGBM Forward & Reverse Prediction Engine
        </div>
        <div style="color:#4A6B5D; margin-bottom:1.5rem; font-size:0.95rem;">
            Perform <b>Forward Predictions</b> (Feature Inputs ➔ Product Category) and <b>Reverse Predictions</b> (Product Class ➔ Feature Profile).
        </div>
        """,
        unsafe_allow_html=True
    )

    model, encoder, reverse_profiles, products_df = load_ml_assets()

    if model is None or encoder is None:
        st.error("⚠️ Model file (`lgbm_multiclass_model.pkl`) or Label Encoder (`label_encoder.pkl`) not found! Please run training script first.")
        return

    st.success("✅ **LightGBM Model, Label Encoder & Reverse Class Profiles loaded successfully!**")

    # Mode Selector Tabs
    tab_forward, tab_reverse = st.tabs(["🔮 Forward Prediction (Features ➔ Product Class)", "🔄 Reverse Prediction (Product Class ➔ Features)"])

    # --- TAB 1: FORWARD PREDICTION ---
    with tab_forward:
        st.markdown("### Forward Prediction: Input Features to Classify Organic Product")
        
        tab_sample, tab_manual = st.tabs(["📋 Select Sample Dataset Row", "⚙️ Custom Feature Inputs"])

        feature_values = {}

        with tab_sample:
            sample_df = load_sample_dataset()
            if sample_df is not None:
                st.markdown("Select a sample transaction record from `Final_Feature_code.csv` to auto-populate features:")
                sample_idx = st.selectbox(
                    "Choose sample row index:",
                    options=list(range(min(50, len(sample_df)))),
                    format_func=lambda i: f"Row #{i} (Actual Product ID: {sample_df.iloc[i]['product_id']})"
                )
                selected_row = sample_df.iloc[sample_idx]
                actual_prod_id = selected_row['product_id']
                actual_name, actual_price, _ = get_product_details(actual_prod_id, products_df)

                st.info(f"📌 **Actual Target in Dataset:** Row #{sample_idx} ➔ `Product ID: {actual_prod_id}` ({actual_name})")

                for col in SELECTED_FEATURES:
                    feature_values[col] = float(selected_row[col])

        with tab_manual:
            st.markdown("Adjust numerical parameters for the 20 SHAP features:")
            col1, col2 = st.columns(2)
            for idx, feature in enumerate(SELECTED_FEATURES):
                default_val = float(feature_values.get(feature, 10.0))
                if idx % 2 == 0:
                    with col1:
                        feature_values[feature] = st.number_input(
                            f"{feature}:", value=default_val, key=f"fwd_inp_{feature}"
                        )
                else:
                    with col2:
                        feature_values[feature] = st.number_input(
                            f"{feature}:", value=default_val, key=f"fwd_inp_{feature}"
                        )

        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)

        if st.button("🔮 Run LightGBM Forward Prediction", use_container_width=True):
            input_data = pd.DataFrame([feature_values])[SELECTED_FEATURES]

            probs = model.predict_proba(input_data)[0]
            top5_indices = np.argsort(probs)[::-1][:5]
            
            best_encoded_class = top5_indices[0]
            best_confidence = probs[best_encoded_class] * 100
            best_prod_id = encoder.inverse_transform([best_encoded_class])[0]

            prod_name, prod_price, cat_id = get_product_details(best_prod_id, products_df)

            st.markdown(
                f"""
                <div style="
                    background: #FFFFFF;
                    border: 2px solid #22C55E;
                    border-radius: 20px;
                    padding: 1.8rem;
                    box-shadow: 0 10px 25px rgba(34, 197, 94, 0.1);
                    margin-bottom: 2rem;
                ">
                    <div style="font-family:'Poppins', sans-serif; font-size:0.85rem; font-weight:700; color:#16A34A; letter-spacing:2px; text-transform:uppercase;">
                        FORWARD MODEL PREDICTION RESULT (TOP-1)
                    </div>
                    <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:800; color:#1B4D3E; margin: 4px 0;">
                        {prod_name}
                    </div>
                    <div style="font-size:1.1rem; color:#0F291E; margin-bottom:12px;">
                        Predicted Product ID: <b>#{best_prod_id}</b> | Category ID: <b>{cat_id}</b> | Price: <b>₹{prod_price:,.2f}</b>
                    </div>
                    <div style="font-size:1.3rem; font-weight:700; color:#15803D;">
                        Model Confidence: {best_confidence:.2f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("#### Top 5 Probable Product Classes Output")
            for rank, encoded_cls in enumerate(top5_indices, 1):
                class_prob = probs[encoded_cls] * 100
                p_id = encoder.inverse_transform([encoded_cls])[0]
                p_name, p_price, _ = get_product_details(p_id, products_df)

                col_rank, col_bar = st.columns([2, 5])
                with col_rank:
                    st.markdown(f"**Rank #{rank}**: `{p_name}` (ID #{p_id})")
                with col_bar:
                    st.progress(float(probs[encoded_cls]))
                    st.caption(f"Probability: **{class_prob:.2f}%** | ₹{p_price:,.2f}")


    # --- TAB 2: REVERSE PREDICTION ---
    with tab_reverse:
        st.markdown("### Reverse Prediction: Select Product to Predict Feature Values Profile")
        
        if reverse_profiles is not None:
            available_pids = sorted(list(reverse_profiles.keys()))
            
            # Format dropdown options with product names from products.csv
            options = []
            for p_id in available_pids:
                p_name, p_price, _ = get_product_details(p_id, products_df)
                options.append((p_id, f"Product #{p_id} — {p_name} (₹{p_price:,.2f})"))

            selected_tuple = st.selectbox(
                "Select Product Class for Reverse Feature Prediction:",
                options=options,
                format_func=lambda x: x[1]
            )
            selected_pid = selected_tuple[0]
            prod_name, prod_price, cat_id = get_product_details(selected_pid, products_df)

            predicted_features = reverse_profiles[selected_pid]

            st.markdown(
                f"""
                <div style="
                    background: #FFFFFF;
                    border: 2px solid #3B82F6;
                    border-radius: 20px;
                    padding: 1.8rem;
                    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1);
                    margin-bottom: 1.5rem;
                ">
                    <div style="font-family:'Poppins', sans-serif; font-size:0.85rem; font-weight:700; color:#2563EB; letter-spacing:2px; text-transform:uppercase;">
                        REVERSE PREDICTION TARGET PRODUCT
                    </div>
                    <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:800; color:#1E3A8A; margin: 4px 0;">
                        {prod_name}
                    </div>
                    <div style="font-size:1.1rem; color:#0F291E;">
                        Selected Product ID: <b>#{selected_pid}</b> | Category ID: <b>{cat_id}</b> | Price: <b>₹{prod_price:,.2f}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("#### Predicted Feature Profile Output (20 SHAP Indicators)")
            
            # Grid display of predicted feature values
            grid_cols = st.columns(4)
            for idx, (feat_name, feat_val) in enumerate(predicted_features.items()):
                col = grid_cols[idx % 4]
                with col:
                    col.metric(
                        label=feat_name,
                        value=f"{feat_val:.4f}"
                    )

            st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)
            
            # Round-trip verification check
            if st.button("🔄 Verify Round-Trip Prediction with LightGBM Model", use_container_width=True):
                rev_df = pd.DataFrame([predicted_features])[SELECTED_FEATURES]
                rev_probs = model.predict_proba(rev_df)[0]
                rev_top1_idx = np.argmax(rev_probs)
                rev_pred_pid = encoder.inverse_transform([rev_top1_idx])[0]
                rev_conf = rev_probs[rev_top1_idx] * 100

                if rev_pred_pid == selected_pid:
                    st.success(f"🎉 **ROUND-TRIP VERIFIED MATCH!** LightGBM classified predicted features back to Product #{rev_pred_pid} ({prod_name}) with **{rev_conf:.2f}%** confidence!")
                else:
                    rev_name, _, _ = get_product_details(rev_pred_pid, products_df)
                    st.warning(f"Round-Trip Result: Classified to Product #{rev_pred_pid} ({rev_name}) with **{rev_conf:.2f}%** confidence.")
        else:
            st.error("Reverse class profiles (`reverse_class_profiles.pkl`) not found.")

if __name__ == '__main__':
    render_ml_prediction_page()
