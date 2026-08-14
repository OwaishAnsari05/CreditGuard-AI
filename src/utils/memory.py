import pandas as pd


def reduce_memory(df):

    """
    Reduce DataFrame Memory Usage
    
    """

    start = df.memory_usage(deep=True).sum() / 1024**2

    for col in df.columns:

        if df[col].dtype == "int64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="integer"
            )

        elif df[col].dtype == "float64":
            df[col] = pd.to_numeric(
                df[col],
                downcast="float"
            )

    end = df.memory_usage(deep=True).sum() / 1024**2

    print(
        f"Memory Reduced : "
        f"{start:.2f} MB → {end:.2f} MB"
    )

    return df