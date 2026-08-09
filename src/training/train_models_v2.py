import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline


# ============================================================
# AI-FRAUDGUARD
# PHASE 3.2
# LEAKAGE-FREE + SMOTE ML PIPELINE
# ============================================================

DATASET_PATH = "dataset/creditcard.csv"
MODEL_DIR = "models/v2"

os.makedirs(MODEL_DIR, exist_ok=True)


print("=" * 75)
print("AI-FRAUDGUARD - PHASE 3.2")
print("SMOTE + LEAKAGE-FREE ML PIPELINE")
print("=" * 75)


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

print("\nLoading raw dataset...")

df = pd.read_csv(DATASET_PATH)

print("✅ Dataset loaded:", df.shape)

print("\nClass Distribution:")

print(df["Class"].value_counts())


# ============================================================
# 2. TIME FEATURE ENGINEERING
# ============================================================

print("\nCreating time features...")

df["Hour"] = (
    df["Time"]
    .str.split(":")
    .str[0]
    .astype(int)
)

df["Minute"] = (
    df["Time"]
    .str.split(":")
    .str[1]
    .astype(int)
)

df["Night_Transaction"] = (
    (df["Hour"] < 6) |
    (df["Hour"] >= 23)
).astype(int)


# ============================================================
# 3. BEHAVIOR FEATURES
# ============================================================

df["New_Device"] = (
    df["Device"].str.lower() == "new"
).astype(int)

df["High_Transaction_Frequency"] = (
    df["Transaction_Count"] >= 15
).astype(int)


# ============================================================
# 4. REMOVE UNNECESSARY COLUMNS
# ============================================================

df = df.drop(
    columns=[
        "Transaction_ID",
        "Time"
    ]
)


# ============================================================
# 5. FEATURES / TARGET
# ============================================================

X = df.drop(columns=["Class"])
y = df["Class"]


print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print("Class")


# ============================================================
# 6. TRAIN TEST SPLIT
# IMPORTANT: BEFORE PREPROCESSING
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining Shape:")
print(X_train.shape)

print("Testing Shape:")
print(X_test.shape)

print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nTesting Class Distribution:")
print(y_test.value_counts())


# ============================================================
# 7. DEFINE FEATURES
# ============================================================

numeric_features = [
    "Amount",
    "Transaction_Count",
    "Account_Age_Days",
    "Hour",
    "Minute",
    "Night_Transaction",
    "New_Device",
    "High_Transaction_Frequency"
]

categorical_features = [
    "Location",
    "Merchant_Category",
    "Device"
]


# ============================================================
# 8. PREPROCESSING
# ============================================================

numeric_transformer = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ============================================================
# 9. MODELS
# ============================================================

models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=400,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBClassifier(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    ),

    "LightGBM": LGBMClassifier(
        n_estimators=400,
        learning_rate=0.05,
        num_leaves=31,
        class_weight="balanced",
        random_state=42,
        verbosity=-1,
        n_jobs=-1
    )
}


# ============================================================
# 10. TRAIN MODELS
# ============================================================

results = {}

best_model = None
best_model_name = None
best_f1 = -1


for name, model in models.items():

    print("\n")
    print("=" * 75)
    print(f"TRAINING {name}")
    print("=" * 75)

    # --------------------------------------------------------
    # Pipeline:
    #
    # Preprocessing
    #      ↓
    # SMOTE
    #      ↓
    # Model
    # --------------------------------------------------------

    pipeline = ImbPipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),

            (
                "smote",
                SMOTE(
                    random_state=42,
                    k_neighbors=5
                )
            ),

            (
                "model",
                model
            )
        ]
    )


    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    pipeline.fit(
        X_train,
        y_train
    )

    print("✅ Training completed")


    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    y_probability = pipeline.predict_proba(
        X_test
    )[:, 1]


    # Default threshold
    threshold = 0.50

    y_pred = (
        y_probability >= threshold
    ).astype(int)


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

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

    pr_auc = average_precision_score(
        y_test,
        y_probability
    )


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred
    )


    print("\n📊 RESULTS")

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    print(
        f"PR-AUC   : {pr_auc:.4f}"
    )


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


    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    filename = (
        name
        .lower()
        .replace(" ", "_")
    )

    model_path = os.path.join(
        MODEL_DIR,
        f"{filename}_smote.pkl"
    )

    joblib.dump(
        pipeline,
        model_path
    )

    print(
        f"💾 Saved: {model_path}"
    )


    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc
    }


    # --------------------------------------------------------
    # SELECT BEST MODEL
    # --------------------------------------------------------

    if f1 > best_f1:

        best_f1 = f1

        best_model = pipeline

        best_model_name = name


# ============================================================
# 11. MODEL COMPARISON
# ============================================================

print("\n")

print("=" * 75)
print("🏆 MODEL COMPARISON")
print("=" * 75)


results_df = pd.DataFrame(
    results
).T


print(
    results_df.round(4)
)


# ============================================================
# 12. SAVE RESULTS
# ============================================================

results_path = os.path.join(
    MODEL_DIR,
    "model_results_v2.csv"
)

results_df.to_csv(
    results_path
)


print(
    f"\n📊 Results saved: {results_path}"
)


# ============================================================
# 13. SAVE BEST MODEL
# ============================================================

best_model_path = os.path.join(
    MODEL_DIR,
    "best_fraud_model_v2.pkl"
)

joblib.dump(
    best_model,
    best_model_path
)


print("\n")

print("=" * 75)
print("🏆 BEST MODEL")
print("=" * 75)

print(
    "Model:",
    best_model_name
)

print(
    f"F1 Score: {best_f1:.4f}"
)

print(
    f"Saved: {best_model_path}"
)


# ============================================================
# 14. FINAL
# ============================================================

print("\n")

print("=" * 75)
print("🎯 PHASE 3.2 COMPLETED SUCCESSFULLY!")
print("=" * 75)