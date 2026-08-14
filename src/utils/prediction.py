import numpy as np


class LoanPredictor:

    def __init__(self, model, preprocessor, threshold):

        self.model = model
        self.preprocessor = preprocessor
        self.threshold = threshold

    def predict(self, input_df):

        # Preprocess Input

        X = self.preprocessor.transform(input_df)

        # Probability

        probability = self.model.predict_proba(X)[0][1]

        print("====================================")
        print("DEBUG PREDICTION")
        print("Threshold:", self.threshold)
        print("Raw probability:", probability)
        print("Probability %:", probability * 100)
        print("Prediction:", int(probability >= self.threshold))
        print("====================================")

        # Apply Threshold

        prediction = int(probability >= self.threshold)

        # Confidence

        confidence = probability if prediction == 1 else (1 - probability)

        confidence = round(confidence * 100, 2)

        probability = round(probability * 100, 2)

        # Risk Level

        if probability < 30:

            risk = "Low Risk"

        elif probability < 60:

            risk = "Medium Risk"

        else:

            risk = "High Risk"

        # Final Decision

        if prediction == 1:

            decision = "Loan Rejected"

            color = "danger"

        else:

            decision = "Loan Approved"

            color = "success"

        # Return Everything

        return {

            "prediction": prediction,

            "decision": decision,

            "probability": probability,

            "confidence": confidence,

            "risk": risk,

            "color": color

        }