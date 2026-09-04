"""
Streamlit UI for LightGBM Multi-Class Product Classifier (100 Organic Product Classes)
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
    """Load LightGBM multiclass model, label encoder, and product catalog."""
    model_path = 'lgbm_multiclass_model.pkl'
    if not os.path.exists(model_path):
        model_path = 'lgbm_model.pkl'

    encoder_path = 'label_encoder.pkl'
    
    model = None
    encoder = None
    products_df = None

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

    if os.path.exists(encoder_path):
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)

    if os.path.exists('products.csv'):
        products_df = pd.read_csv('products.csv')

    return model, encoder, products_df


@st.cache_data
def load_sample_dataset():
    """Load small preview sample of Final_Feature_code.csv for quick UI selection."""
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
            🤖 LightGBM Multi-Class Product Classifier
        </div>
        <div style="color:#4A6B5D; margin-bottom:1.5rem; font-size:0.95rem;">
            Predict real-time organic product classifications across <b>100 target product classes</b> using trained LightGBM GBDT model.
        </div>
        """,
        unsafe_allow_html=True
    )

    model, encoder, products_df = load_ml_assets()

    if model is None or encoder is None:
        st.error("⚠️ Model file (`lgbm_multiclass_model.pkl`) or Label Encoder (`label_encoder.pkl`) not found! Please run training script first.")
        return

    st.success("✅ **LightGBM Multi-Class Model & Label Encoder loaded successfully!**")

    # Sample Data Selector vs Manual Sliders Tab
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

            st.info(f"📌 **Actual Class in Dataset:** Row #{sample_idx} ➔ `Product ID: {actual_prod_id}` ({actual_name})")

            for col in SELECTED_FEATURES:
                feature_values[col] = float(selected_row[col])
        else:
            st.warning("`Final_Feature_code.csv` not found in root workspace.")

    with tab_manual:
        st.markdown("Adjust numerical parameters for the 20 SHAP features:")
        col1, col2 = st.columns(2)
        for idx, feature in enumerate(SELECTED_FEATURES):
            default_val = float(feature_values.get(feature, 10.0))
            if idx % 2 == 0:
                with col1:
                    feature_values[feature] = st.number_input(
                        f"{feature}:", value=default_val, key=f"inp_{feature}"
                    )
            else:
                with col2:
                    feature_values[feature] = st.number_input(
                        f"{feature}:", value=default_val, key=f"inp_{feature}"
                    )

    st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)

    # Predict Button
    if st.button("🔮 Run LightGBM Multi-Class Prediction", use_container_width=True):
        input_data = pd.DataFrame([feature_values])[SELECTED_FEATURES]

        # Model Inference
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
                    MODEL PREDICTION RESULT (TOP-1)
                </div>
                <div style="font-family:'Poppins', sans-serif; font-size:2rem; font-weight:800; color:#1B4D3E; margin: 4px 0;">
                    {prod_name}
                </div>
                <div style="font-size:1.1rem; color:#0F291E; margin-bottom:12px;">
                    Predicted Product ID: <b>#{best_prod_id}</b> | Category ID: <b>{cat_id}</b> | Unit Price: <b>₹{prod_price:,.2f}</b>
                </div>
                <div style="font-size:1.3rem; font-weight:700; color:#15803D;">
                    Model Confidence: {best_confidence:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='font-family:\"Poppins\", sans-serif; font-size:1.3rem; font-weight:700; color:#1B4D3E; margin-bottom:1rem;'>📊 Top 5 Probable Product Class Output</div>", unsafe_allow_html=True)

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

        st.markdown("<hr style='border:0; height:1px; background:#E2E9E3; margin:1.5rem 0;'>", unsafe_allow_html=True)
        st.info("💡 **Tip**: LightGBM outputs Softmax class probabilities across all 100 product categories simultaneously.")


if __name__ == '__main__':
    render_ml_prediction_page()
