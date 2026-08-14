"""
Project Configuration File
"""

DB_USER = "postgres"
DB_PASSWORD = "Owaish05"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credit_risk_db"


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)



RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
MODEL_PATH = "models/"
REPORT_PATH = "reports/"