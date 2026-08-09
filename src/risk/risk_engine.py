# ============================================================
# AI-FRAUDGUARD
# RISK SCORING ENGINE
# ============================================================


def calculate_risk(transaction, ml_result):

    # --------------------------------------------------------
    # ML Risk Score
    # --------------------------------------------------------

    score = float(
        ml_result.get("risk_score", 0)
    )

    reasons = []


    # ========================================================
    # 1. TRANSACTION AMOUNT
    # ========================================================

    amount = float(
        transaction.get("Amount", 0)
    )

    if amount >= 100000:

        score += 15

        reasons.append(
            "Extremely high transaction amount"
        )

    elif amount >= 50000:

        score += 10

        reasons.append(
            "Very high transaction amount"
        )

    elif amount >= 30000:

        score += 6

        reasons.append(
            "High transaction amount"
        )


    # ========================================================
    # 2. NEW DEVICE
    # ========================================================

    device = str(
        transaction.get("Device", "")
    ).lower()

    if device == "new":

        score += 10

        reasons.append(
            "Transaction from a new device"
        )


    # ========================================================
    # 3. TRANSACTION TIME
    # ========================================================

    hour = int(
        transaction.get("Hour", 0)
    )

    if hour < 6 or hour >= 23:

        score += 10

        reasons.append(
            "Unusual transaction time"
        )


    # ========================================================
    # 4. TRANSACTION FREQUENCY
    # ========================================================

    transaction_count = int(
        transaction.get(
            "Transaction_Count",
            0
        )
    )

    if transaction_count >= 25:

        score += 15

        reasons.append(
            "Extremely high transaction frequency"
        )

    elif transaction_count >= 20:

        score += 10

        reasons.append(
            "Very high transaction frequency"
        )

    elif transaction_count >= 15:

        score += 6

        reasons.append(
            "High transaction frequency"
        )


    # ========================================================
    # 5. ACCOUNT AGE
    # ========================================================

    account_age = int(
        transaction.get(
            "Account_Age_Days",
            0
        )
    )

    if account_age <= 30:

        score += 10

        reasons.append(
            "Very new account"
        )

    elif account_age <= 90:

        score += 7

        reasons.append(
            "Young account"
        )

    elif account_age <= 180:

        score += 3

        reasons.append(
            "Relatively young account"
        )


    # ========================================================
    # 6. MERCHANT CATEGORY
    # ========================================================

    merchant = str(
        transaction.get(
            "Merchant_Category",
            ""
        )
    ).lower()

    if merchant == "electronics":

        score += 3

        reasons.append(
            "High-value electronics transaction"
        )

    elif merchant == "travel":

        score += 2

        reasons.append(
            "Travel-related transaction"
        )


    # ========================================================
    # 7. ML FRAUD PREDICTION
    # ========================================================

    prediction = int(
        ml_result.get(
            "prediction",
            0
        )
    )

    probability = float(
        ml_result.get(
            "fraud_probability",
            0
        )
    )

    if prediction == 1:

        score += 10

        reasons.append(
            "Machine learning model flagged transaction"
        )

    elif probability >= 15:

        score += 5

        reasons.append(
            "Elevated ML fraud probability"
        )


    # ========================================================
    # 8. LIMIT SCORE
    # ========================================================

    score = min(
        round(score, 2),
        100.0
    )


    # ========================================================
    # 9. RISK LEVEL
    # ========================================================

    if score >= 80:

        risk_level = "CRITICAL"

    elif score >= 60:

        risk_level = "HIGH"

    elif score >= 30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # ========================================================
    # 10. STATUS
    # ========================================================

    if risk_level == "CRITICAL":

        status = "BLOCK_AND_INVESTIGATE"

    elif risk_level == "HIGH":

        status = "INVESTIGATION_REQUIRED"

    elif risk_level == "MEDIUM":

        status = "MANUAL_REVIEW"

    else:

        status = "NORMAL"


    # ========================================================
    # 11. IF NO REASONS
    # ========================================================

    if not reasons:

        reasons.append(
            "No significant risk indicators detected"
        )


    # ========================================================
    # 12. FINAL RESULT
    # ========================================================

    return {

        "risk_score": score,

        "risk_level": risk_level,

        "status": status,

        "reasons": reasons
    }


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

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


    test_ml_result = {

        "fraud_probability": 72.5,

        "prediction": 1,

        "risk_score": 72.5,

        "threshold": 0.19
    }


    result = calculate_risk(
        test_transaction,
        test_ml_result
    )


    print("\n" + "=" * 60)
    print("AI-FRAUDGUARD RISK ENGINE")
    print("=" * 60)

    print(
        "\nRisk Score:",
        result["risk_score"],
        "/ 100"
    )

    print(
        "Risk Level:",
        result["risk_level"]
    )

    print(
        "Status:",
        result["status"]
    )

    print("\nRisk Reasons:")

    for reason in result["reasons"]:

        print(
            "⚠️",
            reason
        )

    print(
        "\n" + "=" * 60
    )