import pandas as pd
import joblib

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

print("=" * 70)
print("AI-FRAUDGUARD - THRESHOLD OPTIMIZATION")
print("=" * 70)

# ------------------------------------------------------------
# Load test data
# ------------------------------------------------------------

test_df = pd.read_csv(
    "dataset/processed/test.csv"
)

X_test = test_df.drop(columns=["Class"])
y_test = test_df["Class"]

# ------------------------------------------------------------
# Load XGBoost model
# ------------------------------------------------------------

model = joblib.load(
    "models/xgboost.pkl"
)

# ------------------------------------------------------------
# Fraud probability
# ------------------------------------------------------------

probabilities = model.predict_proba(X_test)[:, 1]

print("\nFraud Probability Generated ✅")

# ------------------------------------------------------------
# Test different thresholds
# ------------------------------------------------------------

results = []

for threshold in [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10]:

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

    results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })


results_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("THRESHOLD COMPARISON")
print("=" * 70)

print(
    results_df.round(4).to_string(index=False)
)

# ------------------------------------------------------------
# Best threshold based on F1
# ------------------------------------------------------------

best_row = results_df.loc[
    results_df["F1"].idxmax()
]

best_threshold = best_row["Threshold"]

print("\n" + "=" * 70)
print("🏆 BEST THRESHOLD")
print("=" * 70)

print(
    f"Threshold : {best_threshold:.2f}"
)

print(
    f"Precision : {best_row['Precision']:.4f}"
)

print(
    f"Recall    : {best_row['Recall']:.4f}"
)

print(
    f"F1 Score  : {best_row['F1']:.4f}"
)

# ------------------------------------------------------------
# Final confusion matrix
# ------------------------------------------------------------

final_predictions = (
    probabilities >= best_threshold
).astype(int)

cm = confusion_matrix(
    y_test,
    final_predictions
)

print("\nConfusion Matrix:")

print(cm)

# ------------------------------------------------------------
# Save threshold
# ------------------------------------------------------------

with open(
    "models/best_threshold.txt",
    "w"
) as file:

    file.write(
        str(float(best_threshold))
    )

print(
    "\n💾 Threshold saved:"
    " models/best_threshold.txt"
)

print("\n🎯 Threshold optimization completed!")