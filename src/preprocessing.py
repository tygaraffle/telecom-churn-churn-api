import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

class DataCleaner(BaseEstimator, TransformerMixin):
    """Clean raw dataframe before encoding"""
    
    def __init__(self):
        # Define binary and multi-category columns
        self.binary_cols = ['gender', 'Partner', 'Dependents', 
                           'PhoneService', 'PaperlessBilling']
        
        self.multi_cat_cols = ['MultipleLines', 'InternetService',
                              'OnlineSecurity', 'OnlineBackup',
                              'DeviceProtection', 'TechSupport',
                              'StreamingTV', 'StreamingMovies',
                              'Contract', 'PaymentMethod']
        
        self.num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
        
    def fit(self, X, y=None):
        return self    # Just learns column names/structure
    
    def transform(self, X): #Applies the cleaning rules
        X = X.copy()
        
        # 1. Drop customerID (not needed for modeling)
        if 'customerID' in X.columns:
            X = X.drop('customerID', axis=1)
        
        # 2. Convert TotalCharges to numeric
        X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')  #Converts TotalCharges to numeric
        X['TotalCharges'] = X['TotalCharges'].fillna(0)  #fill in blanks with 0
        
        # 3. Convert SeniorCitizen from int64 to object(strings) for consistent encoding
        # (We'll treat it as categorical even though it's 0/1)
        X['SeniorCitizen'] = X['SeniorCitizen'].astype(str)
        
        return X




def create_preprocessing_pipeline():
    """Build the complete preprocessing pipeline"""
    
    # Define column groups (must match DataCleaner)
    binary_cols = ['gender', 'Partner', 'Dependents', 
                   'PhoneService', 'PaperlessBilling']
    
    multi_cat_cols = ['MultipleLines', 'InternetService',
                      'OnlineSecurity', 'OnlineBackup',
                      'DeviceProtection', 'TechSupport',
                      'StreamingTV', 'StreamingMovies',
                      'Contract', 'PaymentMethod', 'SeniorCitizen']
    
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    
    # Binary encoding: Yes/No → 1/0
    binary_transformer = Pipeline(steps=[
        ('binary_encoder', OneHotEncoder(drop='if_binary', sparse_output=False))
    ])
    
    # Multi-category encoding: One-hot
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Numeric scaling: Standardization
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # Combine everything
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('binary', binary_transformer, binary_cols),
            ('cat', categorical_transformer, multi_cat_cols)
        ],
        remainder='drop'  # Drop any columns not specified
    )
    
    # FULL PIPELINE: Clean → Encode/Scale
    full_pipeline = Pipeline(steps=[
        ('cleaner', DataCleaner()),
        ('preprocessor', preprocessor)
    ])
    
    return full_pipeline

#IMP:So now my data or each row goes thru the data cleaner and then the pipeline(that does the one hot encoding and binary transition and scaling of the data).