from flask import Flask, render_template, request, send_file
from src.utils.model_loader import ModelLoader
from src.utils.prepare_input import PrepareInput
from src.utils.prediction import LoanPredictor
from src.utils.ui_metrics import calculate_dashboard_metrics
from src.utils.decision_summary import generate_decision_summary
from src.utils.pdf_report import PDFReport
from src.services.history_service import HistoryService
from src.utils.shap_explainer import SHAPExplainer

# Flask App

app = Flask(__name__)

# ==========================================================
# Indian Currency Formatter
# ==========================================================

@app.template_filter("inr")
def format_inr(value):

    try:
        value = float(value)

        # Handle decimals
        if value.is_integer():
            number = str(int(value))
            decimal = ""
        else:
            number = f"{value:.2f}"
            number, decimal = number.split(".")

        # Handle negative numbers
        negative = number.startswith("-")

        if negative:
            number = number[1:]

        # Indian numbering system
        if len(number) > 3:

            last_three = number[-3:]
            remaining = number[:-3]

            parts = []

            while len(remaining) > 2:
                parts.insert(0, remaining[-2:])
                remaining = remaining[:-2]

            if remaining:
                parts.insert(0, remaining)

            formatted = ",".join(parts) + "," + last_three

        else:
            formatted = number

        if negative:
            formatted = "-" + formatted

        if decimal:
            formatted = formatted + "." + decimal

        return "₹" + formatted

    except (ValueError, TypeError):
        return value

# Global storage for report generation
latest_report = None

# Load Model 

loader = ModelLoader()
model, preprocessor, threshold, feature_names = loader.load()

prepare = PrepareInput()

predictor = LoanPredictor(
    model=model,
    preprocessor=preprocessor,
    threshold=threshold
)

shap_explainer = SHAPExplainer(
    model=model,
    preprocessor=preprocessor,
    feature_names=feature_names
)

pdf_generator = PDFReport()
history = HistoryService()

# Home Page

@app.route("/")
def home():
    return render_template("index.html")

# Loan Application Page

@app.route("/application")
def application():
    return render_template("predict.html")


# Prediction

@app.route("/predict", methods=["POST"])
def predict():
    try:
        
        # Applicant Information
        
        applicant_name = request.form.get("name")
        phone = request.form.get("phone")
        age = int(request.form.get("age"))
        credit_score = int(request.form.get("credit_score"))

        # Financial Information
        
        income = float(request.form.get("income"))
        dti_ratio = float(request.form.get("dti_ratio"))

        # Loan Information
        
        loan_amount = float(request.form.get("loan_amount"))
        interest_rate = float(request.form.get("interest_rate"))
        loan_term = int(request.form.get("loan_term"))
        purpose = request.form.get("purpose")

        # Dashboard Metrics
       
        metrics = calculate_dashboard_metrics(
            income=income,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_term=loan_term,
            credit_score=credit_score
        )

        # Prepare Model Input
        input_df = prepare.create_dataframe(
            income=income,
            loan_amount=loan_amount,
            credit_score=credit_score,
            interest_rate=interest_rate,
            loan_term=loan_term,
            dti_ratio=dti_ratio,
            age=age
        )

        # Prediction
        result = predictor.predict(input_df)

        # Decision Summary
      
        decision_summary = generate_decision_summary(
            credit_score=credit_score,
            metrics=metrics,
            result=result
        )

        # Save Prediction History
        history.save_prediction(
            applicant_name=applicant_name,
            phone=phone,
            purpose=purpose,
            age=age,
            income=income,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_term=loan_term,
            credit_score=credit_score,
            result=result
        )

        # Decision Explanation
        # ======================
        if result["prediction"] == 0:
            if credit_score >= 700:
                decision_reason = "Loan approved because the applicant has a strong credit score."
            elif metrics.get("dti", 0) < 35:
                decision_reason = "Loan approved because the debt-to-income ratio is healthy."
            elif income >= 1000000:
                decision_reason = "Loan approved because the applicant has a stable annual income."
            else:
                decision_reason = "Loan approved because the overall credit risk is low."
        else:
            if credit_score < 600:
                decision_reason = "Loan rejected because the credit score is below the acceptable limit."
            elif metrics.get("dti", 0) > 50:
                decision_reason = "Loan rejected because the debt-to-income ratio is too high."
            elif income < 300000:
                decision_reason = "Loan rejected because the annual income is insufficient."
            else:
                decision_reason = "Loan rejected because the overall credit risk is high."

        # Result Page
       
        global latest_report
        latest_report = {
            "applicant_name": applicant_name,
            "phone": phone,
            "purpose": purpose,
            "age": age,
            "income": income,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "loan_term": loan_term,
            "metrics": metrics,
            "result": result,
            "decision_summary": decision_summary,
            "decision_reason": decision_reason
        }

        return render_template(
            "result.html",
            applicant_name=applicant_name,
            phone=phone,
            purpose=purpose,
            metrics=metrics,
            result=result,
            decision_summary=decision_summary,
            decision_reason=decision_reason,
            #top_features=top_features.to_dict("records")
        )

    except Exception as e:
        print(e)
        return render_template(
            "error.html",
            error=str(e)
        )


# Download PDF Reports

@app.route("/download_report")
def download_report():
    global latest_report

    if latest_report is None:
        return "No report available. Please make a prediction first."

    filename = "AI_Credit_Report.pdf"

    pdf_generator.generate(
        filename=filename,
        applicant_name=latest_report["applicant_name"],
        phone=latest_report["phone"],
        purpose=latest_report["purpose"],
        age=latest_report["age"],
        income=latest_report["income"],
        loan_amount=latest_report["loan_amount"],
        interest_rate=latest_report["interest_rate"],
        loan_term=latest_report["loan_term"],
        metrics=latest_report["metrics"],
        result=latest_report["result"],
        decision_summary=latest_report["decision_summary"]
    )

    return send_file(
        filename,
        as_attachment=True
    )


# Prediction History

@app.route("/history")
def history_page():
    predictions = history.get_all_predictions()

    return render_template(
        "history.html",
        predictions=predictions
    )


# Run

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )