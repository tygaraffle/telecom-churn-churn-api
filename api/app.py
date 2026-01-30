from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from typing import List

# Load the saved pipeline
MODEL_PATH = "models/churn_pipeline.pkl"
print(f"Loading model from: {MODEL_PATH}")

pipeline = joblib.load(MODEL_PATH)
print("Model loaded successfully!")


# Create FastAPI app
app = FastAPI(
    title="Telecom Churn Prediction API",
    description="API to predict customer churn for telecom company",
    version="1.0"
)


# ========== DATA MODELS ==========
class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: str  # Can be empty string for new customers!


class Prediction(BaseModel):
    churn_prediction: str  # "Churn" or "No Churn"
    churn_probability: float  # 0.0 to 1.0
    risk_level: str  # "Low", "Medium", "High"



# ========== ENDPOINTS ==========
@app.get("/")
def home():
    return {
        "message": "Welcome to Telecom Churn Prediction API",
        "endpoints": {
            "GET /": "This info page",
            "GET /health": "Check API health",
            "POST /predict": "Predict for single customer",
            "POST /predict_batch": "Predict for multiple customers"
        }
    }

@app.get("/health")
def health_check():
    """Check if API and model are working"""
    try:
        # Quick test prediction
        test_data = pd.DataFrame([{
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "tenure": 1,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "No",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 29.85,
            "TotalCharges": "29.85"
        }])
        
        _ = pipeline.predict(test_data)
        
        return {
            "status": "healthy",
            "model": "loaded",
            "model_type": str(type(pipeline)),
            "timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model": "error"
        }
    
@app.post("/predict", response_model=Prediction)
def predict_single(customer: Customer):
    """
    Predict churn for a single customer
    """
    # Convert to DataFrame (our pipeline expects this)
    customer_dict = customer.dict()
    df = pd.DataFrame([customer_dict])
    
    # Make prediction
    probability = pipeline.predict_proba(df)[0, 1]  # Probability of churn
    prediction = pipeline.predict(df)[0]  # 0 or 1
    
    # Determine risk level
    if probability >= 0.7:
        risk = "High"
    elif probability >= 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return Prediction(
        churn_prediction="Churn" if prediction == 1 else "No Churn",
        churn_probability=float(probability),
        risk_level=risk
    )

@app.post("/predict_batch")
def predict_batch(customers: List[Customer]):
    """
    Predict churn for multiple customers at once
    """
    # Convert to DataFrame
    data = [c.dict() for c in customers]
    df = pd.DataFrame(data)
    
    # Make predictions
    probabilities = pipeline.predict_proba(df)[:, 1]
    predictions = pipeline.predict(df)
    
    # Prepare results
    results = []
    for i, (prob, pred) in enumerate(zip(probabilities, predictions)):
        if prob >= 0.7:
            risk = "High"
        elif prob >= 0.4:
            risk = "Medium"
        else:
            risk = "Low"
            
        results.append({
            "customer_id": i + 1,
            "churn_prediction": "Churn" if pred == 1 else "No Churn",
            "churn_probability": float(prob),
            "risk_level": risk
        })
    
    return {
        "predictions": results,
        "total_customers": len(results),
        "summary": {
            "total_churn_risk": sum(1 for r in results if r["churn_prediction"] == "Churn"),
            "high_risk_customers": sum(1 for r in results if r["risk_level"] == "High")
        }
    }