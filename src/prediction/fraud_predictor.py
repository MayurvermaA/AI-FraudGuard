import os
import joblib
import pandas as pd


# ============================================================
# AI-FRAUDGUARD
# FRAUD PREDICTION ENGINE
# ============================================================

MODEL_PATH = "models/v2/lightgbm_smote.pkl"
THRESHOLD_PATH = "models/v2/best_threshold_v2.txt"


class FraudPredictor:

    def __init__(self):

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}"
            )

        # Load trained pipeline
        self.model = joblib.load(MODEL_PATH)

        # Load optimized threshold
        if os.path.exists(THRESHOLD_PATH):

            with open(
                THRESHOLD_PATH,
                "r"
            ) as file:

                self.threshold = float(
                    file.read().strip()
                )

        else:

            # Fallback
            self.threshold = 0.19


    def predict(self, transaction):

        """
        transaction must contain:

        Amount
        Location
        Device
        Transaction_Count
        Merchant_Category
        Account_Age_Days
        Hour
        Minute
        """

        # Convert dictionary to DataFrame
        df = pd.DataFrame(
            [transaction]
        )

        # ----------------------------------------------------
        # Feature Engineering
        # ----------------------------------------------------

        df["Night_Transaction"] = (
            (df["Hour"] < 6) |
            (df["Hour"] >= 23)
        ).astype(int)

        df["New_Device"] = (
            df["Device"]
            .str.lower()
            == "new"
        ).astype(int)

        df["High_Transaction_Frequency"] = (
            df["Transaction_Count"] >= 15
        ).astype(int)

        # ----------------------------------------------------
        # ML Probability
        # ----------------------------------------------------

        probability = self.model.predict_proba(
            df
        )[:, 1][0]

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = int(
            probability >= self.threshold
        )

        # ----------------------------------------------------
        # Risk Score
        # ----------------------------------------------------

        risk_score = round(
            probability * 100,
            2
        )

        return {
            "fraud_probability": round(
                probability * 100,
                2
            ),

            "prediction": prediction,

            "threshold": self.threshold,

            "risk_score": risk_score
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    predictor = FraudPredictor()

    test_transaction = {

        "Amount": 85000,

        "Location": "Mumbai",

        "Device": "New",

        "Transaction_Count": 18,

        "Merchant_Category": "Electronics",

        "Account_Age_Days": 120,

        "Hour": 2,

        "Minute": 14
    }

    result = predictor.predict(
        test_transaction
    )

    print("\n" + "=" * 60)
    print("AI-FRAUDGUARD PREDICTION")
    print("=" * 60)

    print(
        "\nFraud Probability:",
        result["fraud_probability"],
        "%"
    )

    print(
        "Risk Score:",
        result["risk_score"]
    )

    print(
        "Threshold:",
        result["threshold"]
    )

    if result["prediction"] == 1:

        print(
            "\n🚨 FRAUD / HIGH RISK"
        )

    else:

        print(
            "\n✅ NORMAL TRANSACTION"
        )