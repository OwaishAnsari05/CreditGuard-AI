"""
Credit Card Balance Feature Engineering

"""

import numpy as np
import pandas as pd

from src.utils.validation import validate_dataframe
from src.utils.memory import reduce_memory


# Validation

def validate_credit_card(df):

    required_columns = [

        "SK_ID_CURR",

        "SK_ID_PREV",

        "MONTHS_BALANCE",

        "AMT_BALANCE",

        "AMT_CREDIT_LIMIT_ACTUAL",

        "AMT_DRAWINGS_CURRENT",

        "AMT_PAYMENT_TOTAL_CURRENT",

        "SK_DPD",

        "SK_DPD_DEF"

    ]

    validate_dataframe(
        df,
        required_columns,
        "credit_card_balance"
    )


# Cleaning

def clean_credit_card(df):

    credit = df.copy()

    credit = reduce_memory(credit)

    return credit



# Row-Level Features

def engineer_credit_card_features(df):

    credit = df.copy()

    credit["BALANCE_LIMIT_RATIO"] = np.where(

        credit["AMT_CREDIT_LIMIT_ACTUAL"] == 0,

        0,

        credit["AMT_BALANCE"]

        /

        credit["AMT_CREDIT_LIMIT_ACTUAL"]

    )

    credit["PAYMENT_BALANCE_RATIO"] = np.where(

        credit["AMT_BALANCE"] == 0,

        0,

        credit["AMT_PAYMENT_TOTAL_CURRENT"]

        /

        credit["AMT_BALANCE"]

    )

    credit["DRAWING_LIMIT_RATIO"] = np.where(

        credit["AMT_CREDIT_LIMIT_ACTUAL"] == 0,

        0,

        credit["AMT_DRAWINGS_CURRENT"]

        /

        credit["AMT_CREDIT_LIMIT_ACTUAL"]

    )

    credit["IS_LATE"] = (

        credit["SK_DPD"] > 0

    ).astype(int)

    credit["IS_SEVERE_LATE"] = (

        credit["SK_DPD_DEF"] > 0

    ).astype(int)

    return credit



# Customer-Level Aggregation

def aggregate_credit_card_features(credit):

    features = credit.groupby(
        "SK_ID_CURR"
    ).agg(

        CREDIT_CARD_RECORDS=("SK_ID_PREV", "count"),

        CREDIT_CARD_LOANS=("SK_ID_PREV", "nunique"),

        BALANCE_MEAN=("AMT_BALANCE", "mean"),

        BALANCE_MAX=("AMT_BALANCE", "max"),

        LIMIT_MEAN=("AMT_CREDIT_LIMIT_ACTUAL", "mean"),

        LIMIT_MAX=("AMT_CREDIT_LIMIT_ACTUAL", "max"),

        DRAWING_MEAN=("AMT_DRAWINGS_CURRENT", "mean"),

        DRAWING_MAX=("AMT_DRAWINGS_CURRENT", "max"),

        PAYMENT_MEAN=("AMT_PAYMENT_TOTAL_CURRENT", "mean"),

        PAYMENT_MAX=("AMT_PAYMENT_TOTAL_CURRENT", "max"),

        BALANCE_LIMIT_RATIO_MEAN=(

            "BALANCE_LIMIT_RATIO",

            "mean"

        ),

        BALANCE_LIMIT_RATIO_MAX=(

            "BALANCE_LIMIT_RATIO",

            "max"

        ),

        PAYMENT_BALANCE_RATIO_MEAN=(

            "PAYMENT_BALANCE_RATIO",

            "mean"

        ),

        DRAWING_LIMIT_RATIO_MEAN=(

            "DRAWING_LIMIT_RATIO",

            "mean"

        ),

        DPD_MEAN=("SK_DPD", "mean"),

        DPD_MAX=("SK_DPD", "max"),

        DPD_DEF_MEAN=("SK_DPD_DEF", "mean"),

        DPD_DEF_MAX=("SK_DPD_DEF", "max"),

        LATE_COUNT=("IS_LATE", "sum"),

        SEVERE_LATE_COUNT=("IS_SEVERE_LATE", "sum")

    ).reset_index()

    features.fillna(0, inplace=True)

    return features



# Ratio Features

def create_ratio_features(features):

    features["LATE_RATIO"] = (

        features["LATE_COUNT"]

        /

        features["CREDIT_CARD_RECORDS"]

    )

    features["SEVERE_LATE_RATIO"] = (

        features["SEVERE_LATE_COUNT"]

        /

        features["CREDIT_CARD_RECORDS"]

    )

    features.replace(

        [np.inf, -np.inf],

        0,

        inplace=True

    )

    features.fillna(0, inplace=True)

    return features



# Complete Pipeline

def create_credit_card_features(df):

    validate_credit_card(df)

    credit = clean_credit_card(df)

    credit = engineer_credit_card_features(
        credit
    )

    features = aggregate_credit_card_features(
        credit
    )

    features = create_ratio_features(
        features
    )

    return features