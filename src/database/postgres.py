import pandas as pd
from sqlalchemy import create_engine, text

import pandas as pd
from sqlalchemy import create_engine, text

from src.config.config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def test_connection():
    engine = get_engine()

    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).fetchone()[0]

    print("Connected Successfully")
    print(version)


def load_table(table_name):

    engine = get_engine()

    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        engine
    )

    print(f"{table_name} Loaded")

    return df


def save_table(df, table_name):

    engine = get_engine()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} Saved")