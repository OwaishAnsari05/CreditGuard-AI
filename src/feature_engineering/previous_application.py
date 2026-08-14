"""
Previous Application Feature Engineering.

Creates customer-level featuresfrom previous_application table.

"""

import numpy as np
import pandas as pd

from src.utils.validation import validate_dataframe
from src.utils.memory import reduce_memory


# Validation

def validate_previous_application(df):

    required_columns = [

        "SK_ID_CURR",

        "SK_ID_PREV",

        "NAME_CONTRACT_STATUS",

        "NAME_CONTRACT_TYPE",

        "AMT_APPLICATION",

        "AMT_CREDIT",

        "AMT_ANNUITY",

        "AMT_GOODS_PRICE",

        "CNT_PAYMENT",

        "DAYS_DECISION"

    ]

    validate_dataframe(

        df,

        required_columns,

        "previous_application"

    )



# Cleaning

def clean_previous_application(df):

    previous = df.copy()

    previous.replace(
        365243,
        np.nan,
        inplace=True
    )

    previous = reduce_memory(previous)

    return previous


# Row-Level Features


def engineer_previous_application_features(df):

    previous = df.copy()

    previous["IS_APPROVED"] = (

        previous["NAME_CONTRACT_STATUS"]

        ==

        "Approved"

    ).astype(int)

    previous["IS_REFUSED"] = (

        previous["NAME_CONTRACT_STATUS"]

        ==

        "Refused"

    ).astype(int)

    previous["IS_CANCELLED"] = (

        previous["NAME_CONTRACT_STATUS"]

        ==

        "Canceled"

    ).astype(int)

    previous["IS_CONSUMER"] = (

        previous["NAME_CONTRACT_TYPE"]

        ==

        "Consumer loans"

    ).astype(int)

    previous["IS_CASH"] = (

        previous["NAME_CONTRACT_TYPE"]

        ==

        "Cash loans"

    ).astype(int)

    previous["APPLICATION_CREDIT_RATIO"] = np.where(

        previous["AMT_CREDIT"] == 0,

        0,

        previous["AMT_APPLICATION"]

        /

        previous["AMT_CREDIT"]

    )

    previous["ANNUITY_CREDIT_RATIO"] = np.where(

        previous["AMT_CREDIT"] == 0,

        0,

        previous["AMT_ANNUITY"]

        /

        previous["AMT_CREDIT"]

    )

    previous["GOODS_CREDIT_RATIO"] = np.where(

        previous["AMT_CREDIT"] == 0,

        0,

        previous["AMT_GOODS_PRICE"]

        /

        previous["AMT_CREDIT"]

    )

    return previous


def aggregate_previous_application_features(previous):

    previous_features = previous.groupby("SK_ID_CURR").agg(

        # Number of previous applications
        PREV_APPLICATION_COUNT=("SK_ID_PREV", "count"),

        # Status
        APPROVED_COUNT=("IS_APPROVED", "sum"),
        REFUSED_COUNT=("IS_REFUSED", "sum"),
        CANCELLED_COUNT=("IS_CANCELLED", "sum"),

        # Contract Types
        CONSUMER_LOAN_COUNT=("IS_CONSUMER", "sum"),
        CASH_LOAN_COUNT=("IS_CASH", "sum"),

        # Amounts
        APPLICATION_AMOUNT_MEAN=("AMT_APPLICATION", "mean"),
        APPLICATION_AMOUNT_MAX=("AMT_APPLICATION", "max"),

        CREDIT_AMOUNT_MEAN=("AMT_CREDIT", "mean"),
        CREDIT_AMOUNT_MAX=("AMT_CREDIT", "max"),

        GOODS_PRICE_MEAN=("AMT_GOODS_PRICE", "mean"),

        ANNUITY_MEAN=("AMT_ANNUITY", "mean"),

        CNT_PAYMENT_MEAN=("CNT_PAYMENT", "mean"),
        CNT_PAYMENT_MAX=("CNT_PAYMENT", "max"),

        DAYS_DECISION_MEAN=("DAYS_DECISION", "mean"),
        DAYS_DECISION_MAX=("DAYS_DECISION", "max"),

        APPLICATION_CREDIT_RATIO_MEAN=(
            "APPLICATION_CREDIT_RATIO",
            "mean"
        ),

        APPLICATION_CREDIT_RATIO_MAX=(
            "APPLICATION_CREDIT_RATIO",
            "max"
        ),

        ANNUITY_CREDIT_RATIO_MEAN=(
            "ANNUITY_CREDIT_RATIO",
            "mean"
        ),

        GOODS_CREDIT_RATIO_MEAN=(
            "GOODS_CREDIT_RATIO",
            "mean"
        )

    ).reset_index()

    previous_features.fillna(0, inplace=True)

    return previous_features


def create_previous_application_features(df):

    validate_previous_application(df)

    previous = clean_previous_application(df)

    previous = engineer_previous_application_features(previous)

    previous_features = aggregate_previous_application_features(previous)

    return previous_features
