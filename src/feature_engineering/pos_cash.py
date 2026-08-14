"""
POS CASH Feature Engineering

"""

import numpy as np
import pandas as pd

from src.utils.validation import validate_dataframe
from src.utils.memory import reduce_memory


# Validation

def validate_pos_cash(df):

    required_columns = [

        "SK_ID_CURR",

        "SK_ID_PREV",

        "MONTHS_BALANCE",

        "CNT_INSTALMENT",

        "CNT_INSTALMENT_FUTURE",

        "SK_DPD",

        "SK_DPD_DEF",

        "NAME_CONTRACT_STATUS"

    ]

    validate_dataframe(
        df,
        required_columns,
        "POS_CASH_balance"
    )


# Cleaning


def clean_pos_cash(df):

    pos = df.copy()

    pos = reduce_memory(pos)

    return pos


# Row Level Features

def engineer_pos_cash_features(df):

    pos = df.copy()

    pos["IS_COMPLETED"] = (
        pos["NAME_CONTRACT_STATUS"] == "Completed"
    ).astype(int)

    pos["IS_ACTIVE"] = (
        pos["NAME_CONTRACT_STATUS"] == "Active"
    ).astype(int)

    pos["IS_SIGNED"] = (
        pos["NAME_CONTRACT_STATUS"] == "Signed"
    ).astype(int)

    pos["IS_DEMAND"] = (
        pos["NAME_CONTRACT_STATUS"] == "Demand"
    ).astype(int)

    pos["IS_LATE"] = (
        pos["SK_DPD"] > 0
    ).astype(int)

    pos["IS_SEVERE_LATE"] = (
        pos["SK_DPD_DEF"] > 0
    ).astype(int)

    return pos


# Aggregation

def aggregate_pos_cash_features(pos):

    pos_features = pos.groupby(
        "SK_ID_CURR"
    ).agg(

        POS_RECORD_COUNT=("SK_ID_PREV", "count"),

        POS_UNIQUE_LOANS=("SK_ID_PREV", "nunique"),

        POS_COMPLETED_COUNT=("IS_COMPLETED", "sum"),

        POS_ACTIVE_COUNT=("IS_ACTIVE", "sum"),

        POS_SIGNED_COUNT=("IS_SIGNED", "sum"),

        POS_DEMAND_COUNT=("IS_DEMAND", "sum"),

        POS_DPD_MEAN=("SK_DPD", "mean"),

        POS_DPD_MAX=("SK_DPD", "max"),

        POS_DPD_DEF_MEAN=("SK_DPD_DEF", "mean"),

        POS_DPD_DEF_MAX=("SK_DPD_DEF", "max"),

        POS_INSTALMENT_MEAN=("CNT_INSTALMENT", "mean"),

        POS_INSTALMENT_MAX=("CNT_INSTALMENT", "max"),

        POS_FUTURE_INSTALMENT_MEAN=("CNT_INSTALMENT_FUTURE", "mean"),

        POS_FUTURE_INSTALMENT_MAX=("CNT_INSTALMENT_FUTURE", "max"),

        MONTHS_BALANCE_MIN=("MONTHS_BALANCE", "min"),

        MONTHS_BALANCE_MAX=("MONTHS_BALANCE", "max"),

        LATE_PAYMENT_COUNT=("IS_LATE", "sum"),

        SEVERE_LATE_PAYMENT_COUNT=("IS_SEVERE_LATE", "sum")

    ).reset_index()

    pos_features.fillna(0, inplace=True)

    return pos_features


# Ratio Features

def create_ratio_features(pos_features):

    features = pos_features.copy()

    features["POS_LATE_RATIO"] = (

        features["LATE_PAYMENT_COUNT"]

        /

        features["POS_RECORD_COUNT"]

    )

    features["POS_SEVERE_LATE_RATIO"] = (

        features["SEVERE_LATE_PAYMENT_COUNT"]

        /

        features["POS_RECORD_COUNT"]

    )

    features.replace(
        [np.inf, -np.inf],
        0,
        inplace=True
    )

    features.fillna(0, inplace=True)

    return features


# Complete Pipeline

def create_pos_cash_features(df):

    validate_pos_cash(df)

    pos = clean_pos_cash(df)

    pos = engineer_pos_cash_features(pos)

    pos_features = aggregate_pos_cash_features(pos)

    pos_features = create_ratio_features(pos_features)

    return pos_features