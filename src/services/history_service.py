from src.database.database import SessionLocal
from src.models.prediction_model import PredictionHistory


class HistoryService:

    def save_prediction(
        self,
        applicant_name,
        phone,
        purpose,
        age,
        income,
        loan_amount,
        interest_rate,
        loan_term,
        credit_score,
        result
    ):
        db = SessionLocal()

        history = PredictionHistory(
            applicant_name=applicant_name,
            phone=phone,
            purpose=purpose,
            age=age,
            income=income,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_term=loan_term,
            credit_score=credit_score,
            probability=result["probability"],
            confidence=result["confidence"],
            decision=result["decision"]
        )

        db.add(history)
        db.commit()
        db.close()

    def get_all_predictions(self):
        db = SessionLocal()

        predictions = (
            db.query(PredictionHistory)
            .order_by(PredictionHistory.prediction_date.desc())
            .all()
        )

        db.close()

        return predictions