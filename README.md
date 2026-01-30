# Telecom Customer Churn Prediction API
End-to-End Machine Learning Project with Deployment

### Project Overview
This project predicts customer churn for a telecom company using machine learning. It follows the complete data science lifecycle from exploratory analysis to production deployment.

### Live Deployment
API Documentation: https://telecom-churn-api.onrender.com/docs

### Business Problem
Telecom companies face high customer churn rates. This solution helps identify at-risk customers for proactive retention strategies, potentially saving millions in lost revenue.

### Project Pipeline
Data Collection → EDA → Data Cleaning → Feature Engineering → 
Model Training → Model Selection → Pipeline Creation → 
API Development → Dockerization → Cloud Deployment

### Key Insights from EDA
High Churn Groups: Month-to-month contracts, electronic check payments

Protective Factors: Long tenure, multiple services, tech support

Risk Indicators: High monthly charges, low tenure, no service bundles


### Technical Implementation
##### Data Preprocessing
##### Handled missing values in 'TotalCharges' column
##### Encoded categorical variables (One-Hot & Label Encoding)
##### Scaled numerical features (StandardScaler)
##### Addressed class imbalance using strategic sampling

### Model Selection Criteria
#### ROC-AUC: > 84%
##### Precision-Recall Balance: Good performance on minority class
##### Production Readiness: Fast inference, low memory


### API Features
##### Real-time Predictions: Single and batch customer predictions

##### Health Monitoring: System status checks

##### Interactive Docs: Auto-generated Swagger UI

##### Error Handling: Robust input validation

### Technologies Used
##### Category	Tools
##### Data Science	pandas, numpy, scikit-learn,
##### Visualization	matplotlib, seaborn
##### ML Tracking	MLflow
##### API Framework	FastAPI, Uvicorn
##### Containerization	Docker
##### Deployment	Render
##### Version Control	Git, GitHub
##### API Endpoints

### Method	Endpoint	Description
##### GET	/	API information
##### GET	/health	System health check
##### POST	/predict	Single customer prediction
##### POST	/predict_batch	Multiple customer predictions

### Business Impact
##### Proactive Retention: Identify at-risk customers before they leave

##### Targeted Marketing: Focus retention efforts on high-risk segments

##### Revenue Protection: Reduce customer acquisition costs by 30-40%

##### Data-Driven Decisions: Replace intuition with predictive analytics

### Lessons Learned
##### Feature Engineering is Critical: Domain knowledge improves model performance

##### Class Imbalance Matters: Strategic handling prevents model bias

##### MLflow Simplifies Tracking: Experiment management saves time

##### Docker Ensures Consistency: "Works only on my machine" is no longer an issue

##### Deployment is Part of ML: Models only create value when in production

##### Future Enhancements
##### Real-time data pipeline integration

##### A/B testing framework for model updates

##### Customer segmentation clustering

##### Retention strategy recommendation engine


