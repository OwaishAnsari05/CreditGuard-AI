import numpy as np


def validate_dataframe(df, required_columns=None, name="DataFrame"):
    """
    Validate dataframe before feature engineering.
    """

    print("=" * 60)
    print(name)
    print("=" * 60)

    print("Shape :", df.shape)

    print("Duplicate Rows :", df.duplicated().sum())

    print("Missing Values :", df.isnull().sum().sum())

    numeric_cols = df.select_dtypes(include=np.number)

    inf_values = np.isinf(numeric_cols).sum().sum()

    print("Infinity Values :", inf_values)

    # Check required columns
    if required_columns is not None:

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if len(missing) > 0:
            raise ValueError(
                f"Missing Columns: {missing}"
            )

        print("Required Columns : OK")

    print("=" * 60)