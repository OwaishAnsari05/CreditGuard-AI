import json
import pandas as pd


class PrepareInput:

    def __init__(self, feature_file="models/feature_names.json"):

        with open(feature_file, "r") as f:
            self.feature_names = json.load(f)

    def create_dataframe(
        self,
        income,
        loan_amount,
        credit_score,
        interest_rate,
        loan_term,
        dti_ratio,
        age
    ):

        # Create every feature with default value

        row = {}

        for feature in self.feature_names:
            row[feature] = 0

        # Replace important features

        row["AMT_INCOME_TOTAL"] = income

        row["AMT_CREDIT"] = loan_amount

        row["AMT_ANNUITY"] = (
            loan_amount / loan_term
            if loan_term > 0 else 0
        )

        row["DAYS_BIRTH"] = -(age * 365)

        # Optional if present
        if "EXT_SOURCE_2" in row:

            row["EXT_SOURCE_2"] = (
                credit_score - 300
            ) / 550

        # Loan term
        if "CNT_PAYMENT_MEAN" in row:
            row["CNT_PAYMENT_MEAN"] = loan_term

        # Interest
        if "RATE_OF_INTEREST" in row:
            row["RATE_OF_INTEREST"] = interest_rate

        # DTI
        if "DEBT_RATIO_MEAN" in row:
            row["DEBT_RATIO_MEAN"] = dti_ratio

        # Convert to dataframe

        df = pd.DataFrame([row])

        return df