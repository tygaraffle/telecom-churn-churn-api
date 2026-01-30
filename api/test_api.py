import requests
import json

# Test data - NEW customer (empty TotalCharges!)
test_customer = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 5,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 89.50,
    "TotalCharges": ""  # NEW CUSTOMER - our pipeline should handle this!
}

print(" Testing FastAPI...")
print("="*50)

# Test 1: Health check
print("1. Testing /health endpoint...")
try:
    health = requests.get("http://localhost:8000/health")
    print(f"   Status: {health.status_code}")
    print(f"   Response: {health.json()}")
except:
    print("    API not running! Start it with: uvicorn api.app:app --reload")

# Test 2: Single prediction
print("\n2. Testing /predict endpoint...")
try:
    response = requests.post(
        "http://localhost:8000/predict",
        json=test_customer,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result['churn_prediction']}")
        print(f"   Probability: {result['churn_probability']:.1%}")
        print(f"   Risk Level: {result['risk_level']}")
    else:
        print(f"   Error: {response.text}")
        
except Exception as e:
    print(f"    Error: {e}")



# Test 3: Batch prediction
print("\n3. Testing /predict_batch endpoint...")
try:
    batch_data = [test_customer, test_customer]  # Same customer twice
    
    response = requests.post(
        "http://localhost:8000/predict_batch",
        json=batch_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200: #200 means server did not crash or give an error
        result = response.json()
        print(f"   Total predictions: {result['total_customers']}")
        print(f"   Churn risks: {result['summary']['total_churn_risk']}")
    else:
        print(f"   Error: {response.text}")
        
except Exception as e:
    print(f"    Error: {e}")

print("\n" + "="*50)
print(" Test complete!")
#print("\n API Documentation available at: http://localhost:8000/docs")


