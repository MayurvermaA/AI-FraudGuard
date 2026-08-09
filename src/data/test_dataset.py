import pandas as pd
import os

DATASET_PATH = "dataset/creditcard.csv"

print("=" * 60)
print("AI-FRAUDGUARD DATASET TEST")
print("=" * 60)

if not os.path.exists(DATASET_PATH):
    print("\n❌ Dataset not found!")
    print("Expected:", DATASET_PATH)
    exit()

df = pd.read_csv(DATASET_PATH)

print("\n✅ Dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nFraud Percentage:")

fraud_percentage = df["Class"].mean() * 100

print(f"{fraud_percentage:.4f}%")