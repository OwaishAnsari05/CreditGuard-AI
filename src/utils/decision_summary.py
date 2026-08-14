def generate_decision_summary(
    credit_score,
    metrics,
    result
):
    """
     Its Generate human-readable AI decision reasons.
    """

    summary = []

    # Credit Score
    if credit_score >= 750:
        summary.append("Excellent credit score.")
    elif credit_score >= 650:
        summary.append("Good credit score.")
    else:
        summary.append("Low credit score increases default risk.")

    # Loan vs Income
    if metrics["loan_vs_income"] <= 12:
        summary.append(
            "Loan amount is within affordable income limits."
        )
    else:
        summary.append(
            "Loan amount is high compared to monthly income."
        )

    # EMI
    if metrics["emi_ratio"] <= 50:
        summary.append(
            "Monthly EMI is affordable."
        )
    else:
        summary.append(
            "Monthly EMI consumes a large portion of income."
        )

    # Affordability
    summary.append(
        f"Loan affordability status: {metrics['affordability']}"
    )

    # Credit Label
    summary.append(
        f"Credit profile: {metrics['credit_label']}"
    )

    # AI Risk
    summary.append(
        f"Overall AI Risk Assessment: {result['risk']}"
    )

    # Final Recommendation
    if result["prediction"] == 0:
        summary.append(
            "AI recommends approving the loan application."
        )
    else:
        summary.append(
            "AI recommends rejecting the loan application."
        )

    return summary