"""
Bureau Balance Features Engineering

This module creates customer-level features from bureau_balance.csv

Workflow

Validation
    
Cleaning
    
Feature Engineering
    
Aggregation
    
Merge with Bureau

"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd


# Validation

def validate_bureau_balance(df: pd.DataFrame) -> None:
    """
    Validate bureau_balance dataframe.
    """

    required_columns = [
        "SK_ID_BUREAU",
        "MONTHS_BALANCE",
        "STATUS"
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if len(missing) > 0:

        raise ValueError(
            f"Missing Columns : {missing}"
        )

    print("=" * 60)
    print("BUREAU BALANCE VALIDATION")
    print("=" * 60)

    print("Shape :", df.shape)
    print("Duplicate :", df.duplicated().sum())
    print("Missing Values")
    print(df.isnull().sum())

    print("=" * 60)

# Cleaning

def clean_bureau_balance(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Clean bureau_balance dataset.
    """

    bureau_balance = df.copy()

    bureau_balance["STATUS"] = (
        bureau_balance["STATUS"]
        .astype(str)
        .str.strip()
    )

    bureau_balance.drop_duplicates(
        inplace=True
    )

    return bureau_balance


# Feature Engineering


def engineer_bureau_balance_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Create row-level features.
    """

    bureau_balance = df.copy()

  
    # Closed Credit
 
    bureau_balance["STATUS_C"] = (
        bureau_balance["STATUS"] == "C"
    ).astype(int)

    # No Loan
    
    bureau_balance["STATUS_X"] = (
        bureau_balance["STATUS"] == "X"
    ).astype(int)

    # Current

    bureau_balance["STATUS_0"] = (
        bureau_balance["STATUS"] == "0"
    ).astype(int)

    # 1-30 Days
    
    bureau_balance["STATUS_1"] = (
        bureau_balance["STATUS"] == "1"
    ).astype(int)

    # 31-60 Days
    
    bureau_balance["STATUS_2"] = (
        bureau_balance["STATUS"] == "2"
    ).astype(int)

    # 61-90 Days
    
    bureau_balance["STATUS_3"] = (
        bureau_balance["STATUS"] == "3"
    ).astype(int)

    # 91-120 Days

    bureau_balance["STATUS_4"] = (
        bureau_balance["STATUS"] == "4"
    ).astype(int)
  
   # >120 Days

    bureau_balance["STATUS_5"] = (
        bureau_balance["STATUS"] == "5"
    ).astype(int)
   
    # Delinquent

    bureau_balance["IS_DELINQUENT"] = (
        bureau_balance["STATUS"]
        .isin(
            [
                "1",
                "2",
                "3",
                "4",
                "5"
            ]
        )
    ).astype(int)

    # Severe Delinquent

    bureau_balance["SEVERE_DELINQUENT"] = (
        bureau_balance["STATUS"]
        .isin(
            [
                "3",
                "4",
                "5"
            ]
        )
    ).astype(int)

    # Numeric DPD Level

    bureau_balance["DPD_LEVEL"] = (
        bureau_balance["STATUS"]
        .replace(
            {
                "X":0,
                "C":0,
                "0":0,
                "1":1,
                "2":2,
                "3":3,
                "4":4,
                "5":5
            }
        )
        .astype(int)
    )

    return bureau_balance

# Aggregation

def aggregate_bureau_balance_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    """ Aggregate bureau_balanceto one row per SK_ID_BUREAU """

    bureau_balance_features = (

        df

        .groupby("SK_ID_BUREAU")

        .agg(

            TOTAL_MONTHS=(
                "MONTHS_BALANCE",
                "count"
            ),

            LATEST_MONTH=(
                "MONTHS_BALANCE",
                "max"
            ),

            OLDEST_MONTH=(
                "MONTHS_BALANCE",
                "min"
            ),

            STATUS_C_COUNT=(
                "STATUS_C",
                "sum"
            ),

            STATUS_X_COUNT=(
                "STATUS_X",
                "sum"
            ),

            STATUS_0_COUNT=(
                "STATUS_0",
                "sum"
            ),

            STATUS_1_COUNT=(
                "STATUS_1",
                "sum"
            ),

            STATUS_2_COUNT=(
                "STATUS_2",
                "sum"
            ),

            STATUS_3_COUNT=(
                "STATUS_3",
                "sum"
            ),

            STATUS_4_COUNT=(
                "STATUS_4",
                "sum"
            ),

            STATUS_5_COUNT=(
                "STATUS_5",
                "sum"
            ),

            DELINQUENT_MONTHS=(
                "IS_DELINQUENT",
                "sum"
            ),

            SEVERE_DELINQUENT_MONTHS=(
                "SEVERE_DELINQUENT",
                "sum"
            ),

            MAX_DPD_LEVEL=(
                "DPD_LEVEL",
                "max"
            ),

            AVG_DPD_LEVEL=(
                "DPD_LEVEL",
                "mean"
            )

        )

        .reset_index()

    )

    return bureau_balance_features

# Ratio Features

def create_ratio_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Create ratio features.
    """

    features = df.copy()

    features["GOOD_PAYMENT_RATIO"] = (

        features["STATUS_0_COUNT"]

        /

        features["TOTAL_MONTHS"]

    )

    features["LATE_PAYMENT_RATIO"] = (

        features["DELINQUENT_MONTHS"]

        /

        features["TOTAL_MONTHS"]

    )

    features["SEVERE_DELAY_RATIO"] = (

        features["SEVERE_DELINQUENT_MONTHS"]

        /

        features["TOTAL_MONTHS"]

    )

    features["CLOSED_RATIO"] = (

        features["STATUS_C_COUNT"]

        /

        features["TOTAL_MONTHS"]

    )

    features["NO_LOAN_RATIO"] = (

        features["STATUS_X_COUNT"]

        /

        features["TOTAL_MONTHS"]

    )

    features.replace(

        [np.inf, -np.inf],

        0,

        inplace=True

    )

    features.fillna(

        0,

        inplace=True

    )

    return features


# Complete Pipeline

def create_bureau_balance_features(df):

    validate_bureau_balance(df)

    bureau_balance = clean_bureau_balance(df)

    bureau_balance = engineer_bureau_balance_features(
        bureau_balance
    )

    bureau_balance_features = aggregate_bureau_balance_features(
        bureau_balance
    )

    # Convert SK_ID_BUREAU → SK_ID_CURR

    from src.database.postgres import load_table

    bureau = load_table("bureau")

    bureau_balance_features = bureau_balance_features.merge(

        bureau[["SK_ID_BUREAU", "SK_ID_CURR"]],

        on="SK_ID_BUREAU",

        how="left"

    )

    # Aggregate to customer level

    bureau_balance_features = (

        bureau_balance_features

        .groupby("SK_ID_CURR")

        .mean(numeric_only=True)

        .reset_index()

    )

    bureau_balance_features.drop(

        columns=["SK_ID_BUREAU"],

        inplace=True,

        errors="ignore"

    )

    bureau_balance_features.fillna(0, inplace=True)

    print("=" * 60)
    print("Bureau Balance Features Created")
    print("=" * 60)
    print(bureau_balance_features.shape)

    return bureau_balance_features