# ========== IMPORTS ==========
import mlflow           # Main MLflow library - "Experiment Tracker"
import mlflow.sklearn   # Special module for sklearn models
from sklearn.metrics import roc_auc_score, recall_score, precision_score
import pandas as pd

# ========== MAIN TRACKING FUNCTION ==========
def track_experiment(model, model_name, X_train, X_test, Y_train, Y_test, params):
    """
    Track ONE model experiment with MLflow
    Think of this as creating a "REPORT CARD" for your model
    
    Parameters:
    - model: Your ML model (LogisticRegression, RandomForest, etc.)
    - model_name: Nickname for this run (e.g., "Logistic_Regression_v1")
    - X_train, Y_train: Training data
    - X_test, Y_test: Testing data  
    - params: Dictionary of model settings (e.g., {'max_iter': 1000})
    """
    
    #  START tracking a new "experiment run"
    # Everything inside this block gets logged to MLflow
    with mlflow.start_run(run_name=model_name):
        
        # ========== STEP 1: LOG PARAMETERS ==========
        # Save MODEL SETTINGS (hyperparameters)
        # Example: {'class_weight': 'balanced', 'max_iter': 1000}
        mlflow.log_params(params)
        #  Why? So you remember WHAT settings gave the best results
        
        
        # ========== STEP 2: TRAIN MODEL ==========
        # Train the model (same as usual)
        model.fit(X_train, Y_train)
        

     # ========== STEP 3: MAKE PREDICTIONS ==========
        # Get predictions from test set
        Y_pred = model.predict(X_test)  # Binary predictions (0 or 1)
        Y_proba = model.predict_proba(X_test)[:, 1]  # Probabilities (0.0 to 1.0)
        

        # ========== STEP 4: CALCULATE METRICS ==========
        # Calculate how GOOD the model is
        metrics = {
            'roc_auc': roc_auc_score(Y_test, Y_proba),      # Overall skill (0-1)
            'recall': recall_score(Y_test, Y_pred),         # % of churners caught
            'precision': precision_score(Y_test, Y_pred),   # % of flags that were correct
            'accuracy': (Y_pred == Y_test).mean()           # % of all correct predictions
        }
        # the important "GRADES" for your model


        # ========== STEP 5: LOG METRICS ==========
        # Save the grades to MLflow
        mlflow.log_metrics(metrics)
        
        
        # ========== STEP 6: LOG THE MODEL ITSELF ==========
        # Save a COPY of the trained model
        mlflow.sklearn.log_model(model, model_name)
        # Why? So you can download and reuse the EXACT model later


        # ========== STEP 7: PRINT RESULT ==========
        # Show quick summary in notebook
        print(f" {model_name}: ROC-AUC = {metrics['roc_auc']:.3f}")
        #  ROC-AUC is the main "skill score" - higher is better!
    
    # Return the trained model and its metrics
    return model, metrics





# ========== BONUS: SIMPLE COMPARISON FUNCTION ==========
def compare_models(models_dict, X_train, X_test, y_train, y_test):
    """
    Compare MULTIPLE models at once
    
    Parameters:
    - models_dict: {'Model1': model_object, 'Model2': model_object}
    - X_train, X_test, y_train, y_test: Data splits
    """
    
    print(" COMPARING MODELS WITH MLFLOW")
    print("="*50)
    
    results = {}
    
    for name, model in models_dict.items():
        print(f"\n Testing: {name}")
        
        # Create simple parameters based on model type
        params = {
            'model_type': type(model).__name__,  # e.g., 'LogisticRegression'
            'model_name': name
        }
        
        # Track this model
        trained_model, metrics = track_experiment(
            model, name, X_train, X_test, y_train, y_test, params
        )
        
        results[name] = metrics
    
    # Show comparison table
    print("\n" + "="*50)
    print(" FINAL COMPARISON")
    print("="*50)
    
    # Create nice table
    comparison_df = pd.DataFrame(results).T  # Transpose: models as rows
    comparison_df = comparison_df.sort_values('roc_auc', ascending=False)
    
    print("\nRanked by ROC-AUC (higher is better):")
    print(comparison_df[['roc_auc', 'recall', 'precision']].round(3))
    
    # Find winner
    winner = comparison_df.index[0]
    winner_score = comparison_df.iloc[0]['roc_auc']
    
    print(f"\n WINNER: {winner} (ROC-AUC: {winner_score:.3f})")
    
    return comparison_df




# ========== HOW TO VIEW RESULTS ==========
def show_mlflow_instructions():
    """
    Print instructions to view MLflow results
    """
    print("\n" + "="*50)
    print("HOW TO VIEW YOUR MLFLOW RESULTS")
    print("="*50)
    print("\n1. Open NEW terminal/Anaconda Prompt")
    print("2. Navigate to your project:")
    print("   cd \"C:\\Users\\User\\Desktop\\Data Science Projects\\3)Telecome-churn-prediction proj\"")
    print("3. Start MLflow UI:")
    print("   mlflow ui --backend-store-uri mlruns --port 5000")
    print("4. Open browser: http://localhost:5000")
    print("\nYou'll see:")
    print("   List of all experiments")
    print("   Side-by-side model comparison")
    print("   Model parameters (settings)")
    print("   Downloadable model files")
    print("   Charts and metrics")
        