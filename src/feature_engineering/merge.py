"""
Merge All Feature Tables

"""

import pandas as pd

from src.database.postgres import load_table
from src.utils.validation import validate_dataframe



def load_feature_tables():

    application = load_table("application_train")

    bureau = load_table("bureau_features")

    bureau_balance = load_table("bureau_balance_features")

    previous = load_table("previous_application_features")

    pos_cash = load_table("pos_cash_features")

    installments = load_table("installment_features")

    credit_card = load_table("credit_card_features")

    return (
        application,
        bureau,
        bureau_balance,
        previous,
        pos_cash,
        installments,
        credit_card
    )




def merge_feature_tables(

    application,

    bureau,

    bureau_balance,

    previous,

    pos_cash,

    installments,

    credit_card

):

    df = application.copy()

    print("Initial Shape :", df.shape)

    df = df.merge(

        bureau,

        on="SK_ID_CURR",

        how="left"

    )

    print("After Bureau :", df.shape)

    df = df.merge(

        bureau_balance,

        on="SK_ID_CURR",

        how="left"

    )

    print("After Bureau Balance :", df.shape)

    df = df.merge(

        previous,

        on="SK_ID_CURR",

        how="left"

    )

    print("After Previous :", df.shape)

    df = df.merge(

        pos_cash,

        on="SK_ID_CURR",

        how="left"

    )

    print("After POS CASH :", df.shape)

    df = df.merge(

        installments,

        on="SK_ID_CURR",

        how="left"

    )

    print("After Installments :", df.shape)

    df = df.merge(

        credit_card,

        on="SK_ID_CURR",

        how="left"

    )

    print("After Credit Card :", df.shape)

    return df



def handle_missing_values(df):

    numeric_columns = df.select_dtypes(

        include=["number"]

    ).columns

    df[numeric_columns] = df[numeric_columns].fillna(0)

    return df




def validate_final_dataset(df):

    validate_dataframe(

        df,

        None,

        "Final Dataset"

    )

    print(

        "Unique Customers :",

        df["SK_ID_CURR"].nunique()

    )

    print(

        "Duplicate Customers :",

        df["SK_ID_CURR"].duplicated().sum()

    )



def create_final_dataset():

    (

        application,

        bureau,

        bureau_balance,

        previous,

        pos_cash,

        installments,

        credit_card

    ) = load_feature_tables()

    final_df = merge_feature_tables(

        application,

        bureau,

        bureau_balance,

        previous,

        pos_cash,

        installments,

        credit_card

    )

    final_df = handle_missing_values(

        final_df

    )

    validate_final_dataset(

        final_df

    )

    return final_df