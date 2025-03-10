import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_sample_data(n_orders=1000, n_products=50, n_customers=200):
    """Generate sample sales data for testing."""
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_orders)
    
    # Generate product data
    products = pd.DataFrame({
        'product_id': range(1, n_products + 1),
        'product_name': [f'Product {i}' for i in range(1, n_products + 1)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_products),
        'price': np.random.uniform(10, 1000, n_products).round(2)
    })
    
    # Generate customer data
    customers = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'customer_name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_customers)
    })
    
    # Generate order data
    orders = pd.DataFrame({
        'order_id': range(1, n_orders + 1),
        'order_date': dates,
        'customer_id': np.random.choice(customers['customer_id'], n_orders),
        'product_id': np.random.choice(products['product_id'], n_orders),
        'quantity': np.random.randint(1, 10, n_orders)
    })
    
    # Merge data
    merged_data = orders.merge(products, on='product_id')
    merged_data = merged_data.merge(customers, on='customer_id')
    
    # Calculate sales
    merged_data['sales'] = merged_data['quantity'] * merged_data['price']
    
    # Add some seasonality
    merged_data['sales'] *= (1 + 0.2 * np.sin(2 * np.pi * merged_data['order_date'].dt.dayofyear / 365))
    
    # Round sales to 2 decimal places
    merged_data['sales'] = merged_data['sales'].round(2)
    
    return merged_data

def main():
    # Create data directory if it doesn't exist
    data_dir = Path("data/processed")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sample data
    print("Generating sample sales data...")
    data = generate_sample_data()
    
    # Save to CSV
    output_file = data_dir / "merged_orders.csv"
    data.to_csv(output_file, index=False)
    print(f"Sample data saved to {output_file}")
    print(f"Shape: {data.shape}")
    print("\nSample of the data:")
    print(data.head())

if __name__ == "__main__":
    main() 