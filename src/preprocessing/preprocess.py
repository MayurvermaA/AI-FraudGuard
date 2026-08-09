import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ============================================================
# AI-FRAUDGUARD - DATA PREPROCESSING
# ============================================================

DATASET_PATH = "dataset/creditcard.csv"

PROCESSED_DIR = "dataset/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)


print("=" * 70)
print("AI-FRAUDGUARD - DATA PREPROCESSING")
print("=" * 70)


# ============================================================
# 1. LOAD DATASET
# ============================================================

if not os.path.exists(DATASET_PATH):
    print("\n❌ Dataset not found!")
    print("Expected path:", DATASET_PATH)
    exit()

df = pd.read_csv(DATASET_PATH)

print("\n✅ Dataset loaded successfully!")

print("\nOriginal Shape:")
print(df.shape)


# ============================================================
# 2. CHECK MISSING VALUES
# ============================================================

print("\nMissing Values:")

missing_values = df.isnull().sum().sum()

print(missing_values)

if missing_values == 0:
    print("✅ No missing values found.")
else:
    print("⚠️ Missing values found.")


# ============================================================
# 3. REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("✅ Duplicate rows removed.")
else:
    print("✅ No duplicates found.")


# ============================================================
# 4. TIME FEATURE ENGINEERING
# ============================================================

print("\nProcessing Time feature...")

df["Hour"] = df["Time"].str.split(":").str[0].astype(int)
df["Minute"] = df["Time"].str.split(":").str[1].astype(int)

# Night transaction flag
df["Night_Transaction"] = (
    (df["Hour"] < 6) |
    (df["Hour"] >= 23)
).astype(int)

print("✅ Time features created.")

print("\nTime Feature Example:")

print(
    df[
        [
            "Time",
            "Hour",
            "Minute",
            "Night_Transaction"
        ]
    ].head()
)


# ============================================================
# 5. DEVICE FEATURE
# ============================================================

print("\nProcessing Device feature...")

df["New_Device"] = (
    df["Device"].str.lower() == "new"
).astype(int)

print("✅ New_Device feature created.")


# ============================================================
# 6. TRANSACTION FREQUENCY FEATURE
# ============================================================

print("\nProcessing transaction frequency...")

df["High_Transaction_Frequency"] = (
    df["Transaction_Count"] >= 15
).astype(int)

print("✅ High_Transaction_Frequency created.")


# ============================================================
# 7. LOCATION ENCODING
# ============================================================

print("\nEncoding Location...")

location_mapping = {
    location: index
    for index, location
    in enumerate(df["Location"].unique())
}

df["Location_Code"] = df["Location"].map(location_mapping)

print("Location Mapping:")
print(location_mapping)


# ============================================================
# 8. MERCHANT CATEGORY ENCODING
# ============================================================

print("\nEncoding Merchant Category...")

merchant_mapping = {
    merchant: index
    for index, merchant
    in enumerate(df["Merchant_Category"].unique())
}

df["Merchant_Category_Code"] = (
    df["Merchant_Category"].map(merchant_mapping)
)

print("Merchant Mapping:")
print(merchant_mapping)


# ============================================================
# 9. SELECT ML FEATURES
# ============================================================

features = [
    "Amount",
    "Transaction_Count",
    "Account_Age_Days",
    "Hour",
    "Minute",
    "Night_Transaction",
    "New_Device",
    "High_Transaction_Frequency",
    "Location_Code",
    "Merchant_Category_Code"
]

target = "Class"


X = df[features]

y = df[target]


print("\nML Features:")
print(features)

print("\nTarget:")
print(target)


# ============================================================
# 10. FEATURE SCALING
# ============================================================

print("\nScaling numerical features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

X_scaled = pd.DataFrame(
    X_scaled,
    columns=features
)

print("✅ Feature scaling completed.")


# ============================================================
# 11. TRAIN TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# ============================================================
# 12. SAVE PROCESSED DATA
# ============================================================

train_data = X_train.copy()
train_data["Class"] = y_train.values

test_data = X_test.copy()
test_data["Class"] = y_test.values

train_path = os.path.join(
    PROCESSED_DIR,
    "train.csv"
)

test_path = os.path.join(
    PROCESSED_DIR,
    "test.csv"
)

train_data.to_csv(
    train_path,
    index=False
)

test_data.to_csv(
    test_path,
    index=False
)


# ============================================================
# 13. SAVE FEATURE DATA
# ============================================================

processed_data = X_scaled.copy()

processed_data["Class"] = y.values

processed_path = os.path.join(
    PROCESSED_DIR,
    "processed_data.csv"
)

processed_data.to_csv(
    processed_path,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)

print("PREPROCESSING COMPLETED SUCCESSFULLY ✅")

print("=" * 70)

print("\nGenerated Files:")

print("1.", train_path)
print("2.", test_path)
print("3.", processed_path)

print("\nFinal Feature Shape:")
print(X_scaled.shape)

print("\nFinal Target Shape:")
print(y.shape)

print("\nClass Distribution:")
print(y.value_counts())

print("\n🎯 Phase 2 preprocessing completed!")