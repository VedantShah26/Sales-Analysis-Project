import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, silhouette_score
import mlflow
import yaml
import os
from typing import Dict, Any, Tuple
import joblib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelTrainer:
    def __init__(self, config_path: str = 'config/config.yaml'):
        """Initialize ModelTrainer with configuration."""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Set up MLflow
        mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
        mlflow.set_experiment(self.config['mlflow']['experiment_name'])
        
        # Load model parameters
        self.xgb_params = self.config['model_params']['xgboost']
        self.kmeans_params = self.config['model_params']['kmeans']

    def train_xgboost(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> xgb.XGBRegressor:
        """Train XGBoost model for sales forecasting."""
        with mlflow.start_run(run_name='xgboost_training'):
            # Log parameters
            mlflow.log_params(self.xgb_params)
            
            # Create and train model
            model = xgb.XGBRegressor(**self.xgb_params)
            model.fit(
                X_train, 
                y_train,
                eval_set=[(X_val, y_val)],
                early_stopping_rounds=10,
                verbose=False
            )
            
            # Make predictions and calculate metrics
            y_pred = model.predict(X_val)
            rmse = np.sqrt(mean_squared_error(y_val, y_pred))
            
            # Log metrics
            mlflow.log_metric('rmse', rmse)
            
            # Save model
            mlflow.xgboost.log_model(model, 'model')
            
            return model

    def train_kmeans(
        self, 
        X: np.ndarray
    ) -> KMeans:
        """Train K-means model for customer segmentation."""
        with mlflow.start_run(run_name='kmeans_training'):
            # Log parameters
            mlflow.log_params(self.kmeans_params)
            
            # Create and train model
            model = KMeans(**self.kmeans_params)
            clusters = model.fit_predict(X)
            
            # Calculate silhouette score
            score = silhouette_score(X, clusters)
            
            # Log metrics
            mlflow.log_metric('silhouette_score', score)
            
            # Save model
            mlflow.sklearn.log_model(model, 'model')
            
            return model

    def save_model(self, model: Any, model_name: str) -> None:
        """Save trained model to disk."""
        model_path = os.path.join(
            self.config['data_paths']['model_artifacts'],
            f'{model_name}.joblib'
        )
        joblib.dump(model, model_path)

def main():
    """Main function to demonstrate usage."""
    trainer = ModelTrainer()
    
    try:
        # Load processed data
        data = pd.read_csv('data/processed/processed_sales_data.csv')
        
        # Prepare data for XGBoost
        X = data[['quantity', 'price', 'year', 'month', 'day', 'day_of_week']]
        y = data['total_sales']
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train XGBoost model
        xgb_model = trainer.train_xgboost(X_train, y_train, X_val, y_val)
        trainer.save_model(xgb_model, 'xgboost_sales_forecast')
        
        # Train K-means model for customer segmentation
        kmeans_features = data[['total_sales', 'quantity', 'price']]
        kmeans_model = trainer.train_kmeans(kmeans_features)
        trainer.save_model(kmeans_model, 'kmeans_customer_segments')
        
        print("Model training completed successfully!")
        
    except Exception as e:
        print(f"Error during model training: {str(e)}")

if __name__ == "__main__":
    main() 