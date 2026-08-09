import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


# ============================================================
# AI-FRAUDGUARD
# PHASE 3 - ML MODEL TRAINING
# ============================================================

TRAIN_PATH = "dataset/processed/train.csv"
TEST_PATH = "dataset/processed/test.csv"

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)


print("=" * 70)
print("AI-FRAUDGUARD - ML FRAUD DETECTION")
print("=" * 70)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("\nLoading training data...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print("✅ Training data loaded:", train_df.shape)
print("✅ Testing data loaded :", test_df.shape)


# ============================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================

X_train = train_df.drop(columns=["Class"])
y_train = train_df["Class"]

X_test = test_df.drop(columns=["Class"])
y_test = test_df["Class"]


print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nTesting Class Distribution:")
print(y_test.value_counts())


# ============================================================
# 3. CALCULATE CLASS IMBALANCE
# ============================================================

normal_count = (y_train == 0).sum()
fraud_count = (y_train == 1).sum()

scale_pos_weight = normal_count / fraud_count

print("\nClass Imbalance:")
print("Normal:", normal_count)
print("Fraud :", fraud_count)
print("Scale Pos Weight:", round(scale_pos_weight, 2))


# ============================================================
# 4. CREATE MODELS
# ============================================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    ),

    "LightGBM": LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        class_weight="balanced",
        random_state=42,
        verbosity=-1,
        n_jobs=-1
    )
}


# ============================================================
# 5. TRAIN MODELS
# ============================================================

results = {}

best_model = None
best_model_name = None
best_f1 = -1


for name, model in models.items():

    print("\n" + "=" * 70)
    print(f"TRAINING: {name}")
    print("=" * 70)

    model.fit(X_train, y_train)

    print("✅ Model training completed.")

    # Prediction
    y_pred = model.predict(X_test)

    # Probability
    y_probability = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    # Confusion Matrix
    cm = confusion_matrix(
        y_test,
        y_pred
    )

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    }

    print("\n📊 Model Performance")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Normal",
                "Fraud"
            ],
            zero_division=0
        )
    )

    # Save individual model
    safe_name = name.lower().replace(" ", "_")

    model_path = os.path.join(
        MODEL_DIR,
        f"{safe_name}.pkl"
    )

    joblib.dump(
        model,
        model_path
    )

    print(f"💾 Model saved: {model_path}")

    # Best model based on F1
    if f1 > best_f1:

        best_f1 = f1
        best_model = model
        best_model_name = name


# ============================================================
# 6. MODEL COMPARISON
# ============================================================

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

results_df = pd.DataFrame(results).T

print(
    results_df.round(4)
)


# ============================================================
# 7. SAVE RESULTS
# ============================================================

results_path = os.path.join(
    MODEL_DIR,
    "model_results.csv"
)

results_df.to_csv(
    results_path
)

print("\n📊 Results saved:")
print(results_path)


# ============================================================
# 8. SAVE BEST MODEL
# ============================================================

best_model_path = os.path.join(
    MODEL_DIR,
    "best_fraud_model.pkl"
)

joblib.dump(
    best_model,
    best_model_path
)

print("\n" + "=" * 70)
print("🏆 BEST MODEL")
print("=" * 70)

print("Model:", best_model_name)
print(f"F1 Score: {best_f1:.4f}")

print("\n💾 Best model saved:")
print(best_model_path)


# ============================================================
# 9. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("🎯 PHASE 3 COMPLETED SUCCESSFULLY!")
print("=" * 70)