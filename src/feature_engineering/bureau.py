"""
Bureau Feature Engineering

"""

import numpy as np
import pandas as pd

from src.utils.validation import validate_dataframe
from src.utils.memory import reduce_memory


# Validation


def validate_bureau(df):

    required_columns = [

        "SK_ID_CURR",
        "SK_ID_BUREAU",
        "CREDIT_ACTIVE",
        "CREDIT_TYPE",
        "DAYS_CREDIT",
        "DAYS_CREDIT_ENDDATE",
        "AMT_CREDIT_SUM",
        "AMT_CREDIT_SUM_DEBT",
        "AMT_CREDIT_SUM_OVERDUE",
        "AMT_ANNUITY",
        "CNT_CREDIT_PROLONG"

    ]

    validate_dataframe(
        df,
        required_columns,
        "bureau"
    )

# Cleaning

def clean_bureau(df):

    bureau = df.copy()

    bureau = reduce_memory(bureau)

    return bureau



# Feature Engineering

def engineer_bureau_features(df):

    bureau = df.copy()

    bureau["IS_ACTIVE"] = (
        bureau["CREDIT_ACTIVE"] == "Active"
    ).astype(int)

    bureau["IS_CLOSED"] = (
        bureau["CREDIT_ACTIVE"] == "Closed"
    ).astype(int)

    bureau["BAD_DEBT"] = (
        bureau["CREDIT_ACTIVE"] == "Bad debt"
    ).astype(int)

    bureau["HAS_PROLONG"] = (
        bureau["CNT_CREDIT_PROLONG"] > 0
    ).astype(int)

    bureau["IS_CONSUMER"] = (
        bureau["CREDIT_TYPE"] == "Consumer credit"
    ).astype(int)

    bureau["IS_MORTGAGE"] = (
        bureau["CREDIT_TYPE"] == "Mortgage"
    ).astype(int)

    bureau["DEBT_RATIO"] = np.where(

        bureau["AMT_CREDIT_SUM"] == 0,

        0,

        bureau["AMT_CREDIT_SUM_DEBT"] /
        bureau["AMT_CREDIT_SUM"]

    )

    bureau["OVERDUE_RATIO"] = np.where(

        bureau["AMT_CREDIT_SUM"] == 0,

        0,

        bureau["AMT_CREDIT_SUM_OVERDUE"] /
        bureau["AMT_CREDIT_SUM"]

    )

    bureau["CREDIT_DURATION"] = (

        bureau["DAYS_CREDIT_ENDDATE"]

        -

        bureau["DAYS_CREDIT"]

    )

    return bureau


# Aggregation

def aggregate_bureau_features(bureau):

    features = bureau.groupby(
        "SK_ID_CURR"
    ).agg(

        BUREAU_RECORD_COUNT=("SK_ID_BUREAU", "count"),

        ACTIVE_CREDIT_COUNT=("IS_ACTIVE", "sum"),

        CLOSED_CREDIT_COUNT=("IS_CLOSED", "sum"),

        BAD_DEBT_COUNT=("BAD_DEBT", "sum"),

        DAYS_CREDIT_MEAN=("DAYS_CREDIT", "mean"),

        DAYS_CREDIT_MAX=("DAYS_CREDIT", "max"),

        DAYS_ENDDATE_MEAN=("DAYS_CREDIT_ENDDATE", "mean"),

        DAYS_ENDDATE_MAX=("DAYS_CREDIT_ENDDATE", "max"),

        CREDIT_SUM_MEAN=("AMT_CREDIT_SUM", "mean"),

        CREDIT_SUM_MAX=("AMT_CREDIT_SUM", "max"),

        CREDIT_DEBT_MEAN=("AMT_CREDIT_SUM_DEBT", "mean"),

        CREDIT_DEBT_MAX=("AMT_CREDIT_SUM_DEBT", "max"),

        CREDIT_OVERDUE_MEAN=("AMT_CREDIT_SUM_OVERDUE", "mean"),

        CREDIT_OVERDUE_MAX=("AMT_CREDIT_SUM_OVERDUE", "max"),

        DEBT_RATIO_MEAN=("DEBT_RATIO", "mean"),

        DEBT_RATIO_MAX=("DEBT_RATIO", "max"),

        OVERDUE_RATIO_MEAN=("OVERDUE_RATIO", "mean"),

        OVERDUE_RATIO_MAX=("OVERDUE_RATIO", "max"),

        ANNUITY_MEAN=("AMT_ANNUITY", "mean"),

        ANNUITY_MAX=("AMT_ANNUITY", "max"),

        CREDIT_DURATION_MEAN=("CREDIT_DURATION", "mean"),

        CREDIT_DURATION_MAX=("CREDIT_DURATION", "max"),

        PROLONG_COUNT=("HAS_PROLONG", "sum"),

        CONSUMER_CREDIT_COUNT=("IS_CONSUMER", "sum"),

        MORTGAGE_COUNT=("IS_MORTGAGE", "sum")

    ).reset_index()

    features.fillna(0, inplace=True)

    return features


# Complete Pipeline

def create_bureau_features(df):

    validate_bureau(df)

    bureau = clean_bureau(df)

    bureau = engineer_bureau_features(bureau)

    bureau_features = aggregate_bureau_features(bureau)

    print("=" * 60)
    print("Bureau Features Created")
    print("=" * 60)
    print(bureau_features.shape)

    return bureau_features