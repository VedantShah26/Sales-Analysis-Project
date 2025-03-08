import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional
import yaml
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataProcessor:
    def __init__(self, config_path: str = 'config/config.yaml'):
        """Initialize DataProcessor with configuration."""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.raw_data_path = self.config['data_paths']['raw_data']
        self.processed_data_path = self.config['data_paths']['processed_data']
        self.scaler = StandardScaler()

    def load_data(self, filename: str) -> pd.DataFrame:
        """Load data from raw data directory."""
        file_path = os.path.join(self.raw_data_path, filename)
        return pd.read_csv(file_path)

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform basic preprocessing steps."""
        # Convert date columns
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
            df['year'] = df['order_date'].dt.year
            df['month'] = df['order_date'].dt.month
            df['day'] = df['order_date'].dt.day
            df['day_of_week'] = df['order_date'].dt.dayofweek

        # Handle missing values
        df = df.fillna({
            'quantity': 0,
            'price': df['price'].mean() if 'price' in df.columns else 0
        })

        # Remove duplicates
        df = df.drop_duplicates()

        return df

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create new features for analysis."""
        if all(col in df.columns for col in ['quantity', 'price']):
            # Calculate total sales
            df['total_sales'] = df['quantity'] * df['price']

            # Calculate moving averages
            df['sales_7d_ma'] = df.groupby('product_id')['total_sales'].transform(
                lambda x: x.rolling(window=7, min_periods=1).mean()
            )

        return df

    def scale_features(self, df: pd.DataFrame, columns_to_scale: list) -> pd.DataFrame:
        """Scale numerical features."""
        df_scaled = df.copy()
        df_scaled[columns_to_scale] = self.scaler.fit_transform(df[columns_to_scale])
        return df_scaled

    def prepare_time_series(
        self, 
        df: pd.DataFrame, 
        target_col: str,
        sequence_length: int = 30
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare time series data for forecasting."""
        data = df[target_col].values
        X, y = [], []
        
        for i in range(len(data) - sequence_length):
            X.append(data[i:(i + sequence_length)])
            y.append(data[i + sequence_length])
            
        return np.array(X), np.array(y)

    def save_processed_data(self, df: pd.DataFrame, filename: str) -> None:
        """Save processed data to the processed data directory."""
        output_path = os.path.join(self.processed_data_path, filename)
        df.to_csv(output_path, index=False)

def main():
    """Main function to demonstrate usage."""
    processor = DataProcessor()
    
    # Example usage
    try:
        # Load data
        df = processor.load_data('sales_data.csv')
        
        # Preprocess
        df = processor.preprocess_data(df)
        
        # Feature engineering
        df = processor.feature_engineering(df)
        
        # Scale features if needed
        numerical_columns = ['quantity', 'price', 'total_sales']
        df_scaled = processor.scale_features(df, numerical_columns)
        
        # Save processed data
        processor.save_processed_data(df_scaled, 'processed_sales_data.csv')
        
        print("Data processing completed successfully!")
        
    except Exception as e:
        print(f"Error during data processing: {str(e)}")

if __name__ == "__main__":
    main() 