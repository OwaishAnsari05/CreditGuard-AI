from src.database.database import Base
from src.database.database import engine

from src.models.prediction_model import PredictionHistory

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")