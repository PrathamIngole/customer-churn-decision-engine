def generate_explanation(probability: float, customer_data: dict) -> str:
    """
    Generate rule-based churn explanation.
    """

    reasons = []

    if customer_data.get("Tenure Months", 0) < 6:
        reasons.append("low tenure")

    if customer_data.get("Contract") == "Month-to-month":
        reasons.append("month-to-month contract")

    if customer_data.get("Tech Support") == "No":
        reasons.append("no tech support")

    if customer_data.get("Monthly Charges", 0) > 80:
        reasons.append("high monthly charges")

    if not reasons:
        return "Customer shows stable profile with low churn indicators."

    if probability >= 0.6:
        prefix = "Customer is at high risk due to "
    elif probability >= 0.35:
        prefix = "Customer shows moderate churn signals including "
    else:
        prefix = "Customer has minor churn indicators such as "
        
    
    return prefix + ", ".join(reasons) + "."


def evaluate_customer(probability: float, customer_data: dict) -> dict:
    """
    Evaluate churn probability and return structured
    business decision output.
    """

    AVERAGE_CLTV = 10000
    THRESHOLD = 0.35

    # Prediction label
    prediction = "Yes" if probability >= THRESHOLD else "No"

    # Risk tier
    if probability >= 0.6:
        risk_tier = "High"
        recommended_action = "Proactive call + contract conversion incentive"
    elif probability >= 0.35:
        risk_tier = "Medium"
        recommended_action = "Engagement email + support bundle offer"
    else:
        risk_tier = "Low"
        recommended_action = "No immediate intervention"

    expected_revenue_at_risk = probability * AVERAGE_CLTV

    explanation = generate_explanation(probability, customer_data)

    return {
        "churn_probability": round(float(probability), 4),
        "churn_prediction": prediction,
        "risk_tier": risk_tier,
        "recommended_action": recommended_action,
        "expected_revenue_at_risk": round(float(expected_revenue_at_risk), 2),
        "explanation" : explanation
    }
