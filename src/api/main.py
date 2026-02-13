from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path
from src.api.schemas import CustomerData
from src.services.decision_engine import evaluate_customer


app = FastAPI(title="Customer Churn Prediction API")

MODEL_PATH = Path("models/logistic_churn_model.joblib")

model = joblib.load(MODEL_PATH)

@app.get("/")
def read_root():
    return {"message" : "Churn Prediction API is running"}

@app.post("/predict")
def predict_churn(customer : CustomerData) :

    # Convert input to dictionary
    input_dict = customer.dict()

    # Map underscore fields back to original training column names
    mapped_input = {
        "Gender": input_dict["Gender"],
        "Senior Citizen": input_dict["Senior_Citizen"],
        "Partner": input_dict["Partner"],
        "Dependents": input_dict["Dependents"],
        "Tenure Months": input_dict["Tenure_Months"],
        "Phone Service": input_dict["Phone_Service"],
        "Multiple Lines": input_dict["Multiple_Lines"],
        "Internet Service": input_dict["Internet_Service"],
        "Online Security": input_dict["Online_Security"],
        "Online Backup": input_dict["Online_Backup"],
        "Device Protection": input_dict["Device_Protection"],
        "Tech Support": input_dict["Tech_Support"],
        "Streaming TV": input_dict["Streaming_TV"],
        "Streaming Movies": input_dict["Streaming_Movies"],
        "Contract": input_dict["Contract"],
        "Paperless Billing": input_dict["Paperless_Billing"],
        "Payment Method": input_dict["Payment_Method"],
        "Monthly Charges": input_dict["Monthly_Charges"],
        "Total Charges": input_dict["Total_Charges"],
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([mapped_input])

    # Predict probability
    probability = model.predict_proba(input_df)[0][1]

    result = evaluate_customer(probability, input_df.iloc[0].to_dict())

    return result


