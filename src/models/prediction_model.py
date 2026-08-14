from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from datetime import datetime

from src.database.database import Base

class PredictionHistory(Base):

    __tablename__ = "prediction_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    applicant_name = Column(String)

    phone = Column(String)

    purpose = Column(String)

    age = Column(Integer)

    income = Column(Float)

    loan_amount = Column(Float)

    interest_rate = Column(Float)

    loan_term = Column(Integer)

    credit_score = Column(Integer)

    probability = Column(Float)

    confidence = Column(Float)

    decision = Column(String)

    prediction_date = Column(
        DateTime,
        default=datetime.utcnow
    )