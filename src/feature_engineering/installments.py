"""
Installments Payments Feature Engineering

"""

import numpy as np
import pandas as pd

from src.utils.validation import validate_dataframe
from src.utils.memory import reduce_memory


# Validation

def validate_installments(df):

    required_columns = [

        "SK_ID_CURR",

        "SK_ID_PREV",

        "NUM_INSTALMENT_VERSION",

        "NUM_INSTALMENT_NUMBER",

        "DAYS_INSTALMENT",

        "DAYS_ENTRY_PAYMENT",

        "AMT_INSTALMENT",

        "AMT_PAYMENT"

    ]

    validate_dataframe(
        df,
        required_columns,
        "installments_payments"
    )


# Cleaning

def clean_installments(df):

    installments = df.copy()

    installments = reduce_memory(installments)

    return installments



# Row-Level Features

def engineer_installments_features(df):

    installments = df.copy()

    # Days difference
    installments["PAYMENT_DELAY"] = (

        installments["DAYS_ENTRY_PAYMENT"]

        -

        installments["DAYS_INSTALMENT"]

    )

    # Amount difference
    installments["PAYMENT_DIFF"] = (

        installments["AMT_PAYMENT"]

        -

        installments["AMT_INSTALMENT"]

    )

    # Payment ratio
    installments["PAYMENT_RATIO"] = np.where(

        installments["AMT_INSTALMENT"] == 0,

        0,

        installments["AMT_PAYMENT"]

        /

        installments["AMT_INSTALMENT"]

    )

    # Late Payment
    installments["IS_LATE"] = (

        installments["PAYMENT_DELAY"] > 0

    ).astype(int)

    # Early Payment
    installments["IS_EARLY"] = (

        installments["PAYMENT_DELAY"] < 0

    ).astype(int)

    # Under Payment
    installments["IS_UNDERPAID"] = (

        installments["AMT_PAYMENT"]

        <

        installments["AMT_INSTALMENT"]

    ).astype(int)

    # Over Payment
    installments["IS_OVERPAID"] = (

        installments["AMT_PAYMENT"]

        >

        installments["AMT_INSTALMENT"]

    ).astype(int)

    return installments



# Customer-Level Aggregation


def aggregate_installments_features(installments):

    features = installments.groupby(
        "SK_ID_CURR"
    ).agg(

        INSTALLMENT_RECORD_COUNT=("SK_ID_PREV", "count"),

        UNIQUE_LOANS=("SK_ID_PREV", "nunique"),

        LATE_PAYMENT_COUNT=("IS_LATE", "sum"),

        EARLY_PAYMENT_COUNT=("IS_EARLY", "sum"),

        UNDERPAID_COUNT=("IS_UNDERPAID", "sum"),

        OVERPAID_COUNT=("IS_OVERPAID", "sum"),

        PAYMENT_DELAY_MEAN=("PAYMENT_DELAY", "mean"),

        PAYMENT_DELAY_MAX=("PAYMENT_DELAY", "max"),

        PAYMENT_DELAY_MIN=("PAYMENT_DELAY", "min"),

        PAYMENT_RATIO_MEAN=("PAYMENT_RATIO", "mean"),

        PAYMENT_RATIO_MAX=("PAYMENT_RATIO", "max"),

        PAYMENT_RATIO_MIN=("PAYMENT_RATIO", "min"),

        PAYMENT_DIFF_MEAN=("PAYMENT_DIFF", "mean"),

        PAYMENT_DIFF_MAX=("PAYMENT_DIFF", "max"),

        AMT_PAYMENT_MEAN=("AMT_PAYMENT", "mean"),

        AMT_PAYMENT_MAX=("AMT_PAYMENT", "max"),

        AMT_INSTALMENT_MEAN=("AMT_INSTALMENT", "mean"),

        AMT_INSTALMENT_MAX=("AMT_INSTALMENT", "max")

    ).reset_index()

    features.fillna(0, inplace=True)

    return features



# Ratio Features


def create_ratio_features(features):

    features["LATE_PAYMENT_RATIO"] = (

        features["LATE_PAYMENT_COUNT"]

        /

        features["INSTALLMENT_RECORD_COUNT"]

    )

    features["UNDERPAID_RATIO"] = (

        features["UNDERPAID_COUNT"]

        /

        features["INSTALLMENT_RECORD_COUNT"]

    )

    features.replace(

        [np.inf, -np.inf],

        0,

        inplace=True

    )

    features.fillna(0, inplace=True)

    return features


# Complete Pipeline


def create_installments_features(df):

    validate_installments(df)

    installments = clean_installments(df)

    installments = engineer_installments_features(
        installments
    )

    features = aggregate_installments_features(
        installments
    )

    features = create_ratio_features(
        features
    )

    return features