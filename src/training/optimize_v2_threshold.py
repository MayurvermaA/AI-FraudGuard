import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    average_precision_score
)

print("=" * 75)
print("AI-FRAUDGUARD - PHASE 3.3")
print("OPTIMAL FRAUD THRESHOLD")
print("=" * 75)


# ============================================================
# LOAD RAW DATA
# ============================================================

df = pd.read_csv(
    "dataset/creditcard.csv"
)

# Time features
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

df["New_Device"] = (
    df["Device"].str.lower() == "new"
).astype(int)

df["High_Transaction_Frequency"] = (
    df["Transaction_Count"] >= 15
).astype(int)

df = df.drop(
    columns=[
        "Transaction_ID",
        "Time"
    ]
)

X = df.drop(columns=["Class"])
y = df["Class"]


# ============================================================
# SAME TRAIN TEST SPLIT
# ============================================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# MODELS
# ============================================================

models = {
    "Random Forest": "models/v2/random_forest_smote.pkl",
    "LightGBM": "models/v2/lightgbm_smote.pkl"
}


# ============================================================
# THRESHOLDS
# ============================================================

thresholds = np.arange(
    0.01,
    0.51,
    0.01
)


all_results = []


# ============================================================
# TEST EACH MODEL
# ============================================================

for model_name, model_path in models.items():

    print("\n")
    print("=" * 75)
    print(model_name)
    print("=" * 75)

    model = joblib.load(model_path)

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    pr_auc = average_precision_score(
        y_test,
        probabilities
    )

    print(
        f"\nPR-AUC: {pr_auc:.4f}"
    )

    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        all_results.append({
            "Model": model_name,
            "Threshold": threshold,
            "Precision": precision,
            "Recall": recall,
            "F1": f1
        })


# ============================================================
# RESULTS
# ============================================================

results_df = pd.DataFrame(
    all_results
)


# ============================================================
# BEST F1
# ============================================================

best_f1 = results_df.loc[
    results_df["F1"].idxmax()
]


print("\n")
print("=" * 75)
print("🏆 BEST F1 THRESHOLD")
print("=" * 75)

print(
    best_f1.to_string()
)


# ============================================================
# BEST RECALL WITH PRECISION >= 10%
# ============================================================

valid = results_df[
    results_df["Precision"] >= 0.10
]

if not valid.empty:

    best_recall = valid.loc[
        valid["Recall"].idxmax()
    ]

    print("\n")
    print("=" * 75)
    print("🎯 BEST RECALL (PRECISION >= 10%)")
    print("=" * 75)

    print(
        best_recall.to_string()
    )


# ============================================================
# SAVE RESULTS
# ============================================================

output_path = (
    "models/v2/threshold_results.csv"
)

results_df.to_csv(
    output_path,
    index=False
)

print(
    f"\n💾 Saved: {output_path}"
)


# ============================================================
# SAVE BEST F1 THRESHOLD
# ============================================================

with open(
    "models/v2/best_threshold_v2.txt",
    "w"
) as f:

    f.write(
        str(
            float(
                best_f1["Threshold"]
            )
        )
    )


# ============================================================
# CONFUSION MATRIX
# ============================================================

best_model_path = models[
    best_f1["Model"]
]

best_model = joblib.load(
    best_model_path
)

best_probabilities = best_model.predict_proba(
    X_test
)[:, 1]

best_predictions = (
    best_probabilities >= best_f1["Threshold"]
).astype(int)

cm = confusion_matrix(
    y_test,
    best_predictions
)

print("\n")
print("=" * 75)
print("CONFUSION MATRIX")
print("=" * 75)

print(cm)


print("\n")
print("=" * 75)
print("🎯 PHASE 3.3 COMPLETED")
print("=" * 75)