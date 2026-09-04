"""
Multi-Class Classification for Organic Food Traceability (>10 Target Classes)
Target: product_id (100 distinct classes)
Models: LightGBM, XGBoost, Random Forest
"""

import pandas as pd
import numpy as np
import pickle
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, top_k_accuracy_score, f1_score,
    precision_score, recall_score, log_loss, classification_report
)
import lightgbm as lgb
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

def main():
    print("="*60)
    print("      MULTI-CLASS CLASSIFICATION PIPELINE (100 CLASSES)      ")
    print("="*60)

    # 1. Load Dataset
    print("\n[1/6] Loading dataset Final_Feature_code.csv...")
    start_time = time.time()
    
    selected_features = [
        'min_pp', 'p90_pp', 'p95_pad', 'p25_pp', 'p95_pp', 'max_pp',
        'min_pad', 'p75_pp', 'max_pad', 'p90_pad', 'avg_pp', 'p50_pp',
        'p25_pad', 'p50_pad', 'avg_pad', 'p75_pad', 'p90_pd', 'total_pad',
        'max_pd', 'p95_pd'
    ]
    target_col = 'product_id'
    
    cols_to_use = selected_features + [target_col]
    df = pd.read_csv('Final_Feature_code.csv', usecols=cols_to_use)
    
    print(f"Data loaded successfully: {df.shape[0]} rows, {len(selected_features)} features.")
    print(f"Time taken to load: {round(time.time() - start_time, 2)}s")

    # Sample data for model training to ensure speed and stability (150,000 samples stratified)
    if len(df) > 150000:
        print("Subsampling 150,000 rows (stratified) for multi-class training...")
        df_sample, _ = train_test_split(
            df, train_size=150000, stratify=df[target_col], random_state=42
        )
    else:
        df_sample = df.copy()

    X = df_sample[selected_features]
    y_raw = df_sample[target_col]

    # 2. Encode Target Classes
    print("\n[2/6] Encoding target variable (product_id)...")
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    num_classes = len(le.classes_)
    print(f"Total Unique Target Classes: {num_classes}")

    # Save LabelEncoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)
    print("Saved label_encoder.pkl")

    # 3. Train / Test Split
    print("\n[3/6] Splitting dataset into train (80%) and test (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")

    models = {}
    metrics = []

    # 4. Model Training & Evaluation
    print("\n[4/6] Training & Evaluating Multi-Class Models...")

    # --- Model A: LightGBM Multiclass Classifier ---
    print("\n--> Training Model 1: LightGBM Multiclass Classifier...")
    t0 = time.time()
    lgbm_model = lgb.LGBMClassifier(
        objective='multiclass',
        num_class=num_classes,
        n_estimators=150,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42,
        verbosity=-1,
        n_jobs=-1
    )
    lgbm_model.fit(X_train, y_train)
    lgbm_train_time = round(time.time() - t0, 2)
    models['LightGBM'] = lgbm_model

    # --- Model B: XGBoost Multiclass Classifier ---
    print("--> Training Model 2: XGBoost Multiclass Classifier...")
    t0 = time.time()
    xgb_model = xgb.XGBClassifier(
        objective='multi:softprob',
        num_class=num_classes,
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        random_state=42,
        n_jobs=-1,
        eval_metric='mlogloss'
    )
    xgb_model.fit(X_train, y_train)
    xgb_train_time = round(time.time() - t0, 2)
    models['XGBoost'] = xgb_model

    # --- Model C: Random Forest Multiclass Classifier ---
    print("--> Training Model 3: Random Forest Multiclass Classifier...")
    t0 = time.time()
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_train_time = round(time.time() - t0, 2)
    models['RandomForest'] = rf_model

    # 5. Evaluate Metrics for All Models
    print("\n[5/6] Comparing Performance Across All Models...")
    
    train_times = {
        'LightGBM': lgbm_train_time,
        'XGBoost': xgb_train_time,
        'RandomForest': rf_train_time
    }

    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)

        acc = accuracy_score(y_test, y_pred)
        top3_acc = top_k_accuracy_score(y_test, y_proba, k=3)
        top5_acc = top_k_accuracy_score(y_test, y_proba, k=5)
        f1_w = f1_score(y_test, y_pred, average='weighted')
        prec_w = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec_w = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        loss = log_loss(y_test, y_proba)

        metrics.append({
            'Model': name,
            'Top-1 Accuracy': round(acc, 4),
            'Top-3 Accuracy': round(top3_acc, 4),
            'Top-5 Accuracy': round(top5_acc, 4),
            'Weighted F1': round(f1_w, 4),
            'Weighted Precision': round(prec_w, 4),
            'Weighted Recall': round(rec_w, 4),
            'Log Loss': round(loss, 4),
            'Train Time (s)': train_times[name]
        })

    results_df = pd.DataFrame(metrics).sort_values('Top-1 Accuracy', ascending=False)
    print("\n" + "="*80)
    print("                     MULTI-CLASS MODEL COMPARISON RESULTS                   ")
    print("="*80)
    print(results_df.to_string(index=False))
    print("="*80)

    # 6. Save Models & Best Artifacts
    print("\n[6/6] Saving Trained Models and Results...")
    
    with open('lgbm_multiclass_model.pkl', 'wb') as f:
        pickle.dump(lgbm_model, f)
    print("Saved lgbm_multiclass_model.pkl")

    with open('xgb_multiclass_model.pkl', 'wb') as f:
        pickle.dump(xgb_model, f)
    print("Saved xgb_multiclass_model.pkl")

    with open('rf_multiclass_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    print("Saved rf_multiclass_model.pkl")

    print("\nDetailed Classification Report for LightGBM Classifier (Top 15 Classes Preview):")
    best_pred = lgbm_model.predict(X_test)
    report_dict = classification_report(y_test, best_pred, output_dict=True, zero_division=0)
    report_df = pd.DataFrame(report_dict).T
    print(report_df.head(15).to_string())

    print("\nMulti-class pipeline execution completed successfully!")

if __name__ == '__main__':
    main()
