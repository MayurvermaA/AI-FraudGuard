import os
import json

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# AI-FRAUDGUARD
# GROQ AI INVESTIGATION ASSISTANT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file"
    )


client = Groq(
    api_key=API_KEY
)


class FraudInvestigator:

    def __init__(self):

        self.model = "openai/gpt-oss-20b"


    def investigate(
        self,
        transaction,
        ml_result,
        risk_result
    ):

        investigation_data = {
            "transaction": transaction,
            "ml_result": ml_result,
            "risk_result": risk_result
        }


        prompt = f"""
You are an AI financial fraud investigation assistant.

Analyze the transaction information below.

Do not claim that a transaction is certainly fraudulent.
Use professional terms such as suspicious,
high-risk, potentially fraudulent, and requires investigation.

Generate a professional investigation report.

Include:

1. Executive Summary
2. Risk Assessment
3. Suspicious Indicators
4. Evidence
5. Recommended Action
6. Analyst Notes

Transaction information:

{json.dumps(
    investigation_data,
    indent=2,
    default=str
)}
"""


        response = client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional financial "
                        "fraud investigation assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1200
        )


        return response.choices[
            0
        ].message.content


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    investigator = FraudInvestigator()


    transaction = {

        "Transaction_ID": "TXN001245",

        "Amount": 85000,

        "Location": "Mumbai",

        "Device": "New",

        "Transaction_Count": 18,

        "Merchant_Category": "Electronics",

        "Account_Age_Days": 120,

        "Hour": 2,

        "Minute": 14
    }


    ml_result = {

        "fraud_probability": 72.5,

        "prediction": 1,

        "risk_score": 72.5,

        "threshold": 0.19
    }


    risk_result = {

        "risk_score": 100,

        "risk_level": "CRITICAL",

        "status": "BLOCK_AND_INVESTIGATE",

        "reasons": [

            "Very high transaction amount",

            "Transaction from a new device",

            "Unusual transaction time",

            "High transaction frequency",

            "Relatively young account",

            "High-value electronics transaction",

            "Machine learning model flagged transaction"
        ]
    }


    print("=" * 70)

    print(
        "🧠 AI-FRAUDGUARD - GROQ INVESTIGATION"
    )

    print("=" * 70)


    report = investigator.investigate(
        transaction,
        ml_result,
        risk_result
    )


    print("\n")
    print(report)


    print("\n")
    print("=" * 70)

    print(
        "✅ AI INVESTIGATION COMPLETED"
    )

    print("=" * 70)