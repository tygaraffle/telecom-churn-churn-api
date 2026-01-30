import streamlit as st
import requests
import pandas as pd

# Page setup
st.set_page_config(page_title="Churn Predictor")

# Title
st.title(" Telecom Churn Predictor")
st.write("Predict if a customer will leave")

# Create input form
st.header("Customer Details")

# Demographics
gender = st.selectbox("Gender", ["Female", "Male"])
senior = st.radio("Senior Citizen", ["No", "Yes"])
partner = st.radio("Partner", ["No", "Yes"])
dependents = st.radio("Dependents", ["No", "Yes"])

# Account info
tenure = st.slider("Tenure (months)", 0, 72, 12)
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless = st.radio("Paperless Billing", ["No", "Yes"])
payment = st.selectbox("Payment", ["Electronic check", "Mailed check", 
                                   "Bank transfer (automatic)", "Credit card (automatic)"])

# Services
phone = st.radio("Phone Service", ["No", "Yes"])
if phone == "Yes":
    lines = st.radio("Multiple Lines", ["No", "Yes", "No phone service"])
else:
    lines = "No phone service"

internet = st.selectbox("Internet", ["DSL", "Fiber optic", "No"])

# Internet services (only show if internet exists)
if internet != "No":
    security = st.radio("Online Security", ["No", "Yes", "No internet service"])
    backup = st.radio("Online Backup", ["No", "Yes", "No internet service"])
    protection = st.radio("Device Protection", ["No", "Yes", "No internet service"])
    support = st.radio("Tech Support", ["No", "Yes", "No internet service"])
    tv = st.radio("Streaming TV", ["No", "Yes", "No internet service"])
    movies = st.radio("Streaming Movies", ["No", "Yes", "No internet service"])
else:
    # If no internet, set all to "No internet service"
    security = backup = protection = support = tv = movies = "No internet service"

# Charges
monthly = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
total = st.number_input("Total Charges", 0.0, 10000.0, tenure * monthly)

# Predict button
st.markdown("---")
if st.button("🔮 Predict Churn", type="primary"):
    
    # Prepare data for your FastAPI
    customer_data = {
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,  # Convert to 0/1
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": lines,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": support,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": str(total)  # String like in your FastAPI
    }
    
    # Show loading
    with st.spinner("Predicting..."):
        try:
            # Call YOUR FastAPI
            response = requests.post(
                "https://telecom-churn-api.onrender.com/predict",
                json=customer_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Show results
                st.success("Done!")
                
                # Prediction
                if result["churn_prediction"] == "Churn":
                    st.error(f"**Prediction:** Will leave")
                else:
                    st.success(f"**Prediction:** Will stay")
                
                # Probability
                prob = result["churn_probability"]
                st.write(f"**Probability:** {prob:.1%}")
                st.progress(prob)
                
                # Risk level
                risk = result["risk_level"]
                if risk == "High":
                    st.error(f"**Risk:** {risk}")
                elif risk == "Medium":
                    st.warning(f"**Risk:** {risk}")
                else:
                    st.success(f"**Risk:** {risk}")
                    
            else:
                st.error("API error")
                
        except:
            st.error("Could not connect to API")

# Sidebar info
with st.sidebar:
    st.write("**About**")
    st.write("Uses your FastAPI with the Kaggle dataset")
    st.write("Model: Random Forest")
    st.write("Accuracy: 86%")
    st.write("---")
    st.write("**API URL:**")
    st.code("https://telecom-churn-api.onrender.com")