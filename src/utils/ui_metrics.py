import math


def calculate_dashboard_metrics(
    income,
    loan_amount,
    interest_rate,
    loan_term,
    credit_score
):
    """
    Calculates all dashboard metrics.

    Parameters
    ----------
    income : float
    loan_amount : float
    interest_rate : float
    loan_term : int
    credit_score : int

    Returns
    -------
    dict
    """

    monthly_income = income / 12

    monthly_rate = interest_rate / 100 / 12

    if monthly_rate == 0:

        monthly_emi = loan_amount / loan_term

    else:

        monthly_emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** loan_term
        ) / (
            (1 + monthly_rate) ** loan_term - 1
        )

    total_payment = monthly_emi * loan_term

    total_interest = total_payment - loan_amount

    loan_vs_income = loan_amount / monthly_income

    emi_ratio = (monthly_emi / monthly_income) * 100

    if emi_ratio <= 30:
        affordability = "Excellent"

    elif emi_ratio <= 40:
        affordability = "Good"

    elif emi_ratio <= 50:
        affordability = "Average"

    else:
        affordability = "Poor"

    if credit_score >= 750:
        credit_label = "Excellent"

    elif credit_score >= 700:
        credit_label = "Good"

    elif credit_score >= 650:
        credit_label = "Fair"

    else:
        credit_label = "Poor"

    return {

        "monthly_income": round(monthly_income,2),

        "monthly_emi": round(monthly_emi,2),

        "total_payment": round(total_payment,2),

        "total_interest": round(total_interest,2),

        "loan_vs_income": round(loan_vs_income,2),

        "emi_ratio": round(emi_ratio,2),

        "affordability": affordability,

        "credit_label": credit_label

    }