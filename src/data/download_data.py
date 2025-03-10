import os
import pandas as pd
import requests
from tqdm import tqdm
import zipfile

def download_file(url: str, filename: str):
    """Download a file from URL with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def main():
    """Main function to download and prepare the dataset."""
    # Create directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)

    # URLs for the dataset files
    base_url = "https://s3.amazonaws.com/instacart-datasets/instacart_online_grocery_shopping_2017_05_01"
    files = [
        "order_products__prior.csv",
        "order_products__train.csv",
        "orders.csv",
        "products.csv",
        "departments.csv",
        "aisles.csv"
    ]

    print("Downloading Instacart dataset files...")
    
    # Download each file
    for file in files:
        url = f"{base_url}/{file}"
        output_path = f"data/raw/{file}"
        
        if not os.path.exists(output_path):
            print(f"\nDownloading {file}...")
            try:
                download_file(url, output_path)
            except Exception as e:
                print(f"Error downloading {file}: {str(e)}")
                continue
        else:
            print(f"\n{file} already exists, skipping download.")

    print("\nPreparing initial dataset...")
    
    try:
        # Load the data
        orders = pd.read_csv('data/raw/orders.csv')
        order_products = pd.read_csv('data/raw/order_products__prior.csv')
        products = pd.read_csv('data/raw/products.csv')
        departments = pd.read_csv('data/raw/departments.csv')
        aisles = pd.read_csv('data/raw/aisles.csv')

        # Merge the dataframes
        df = order_products.merge(orders, on='order_id')
        df = df.merge(products, on='product_id')
        df = df.merge(departments, on='department_id')
        df = df.merge(aisles, on='aisle_id')

        # Save the merged dataset
        df.to_csv('data/processed/merged_orders.csv', index=False)
        print("\nInitial dataset preparation completed!")
        
        # Create a sample of the data for quick testing
        sample = df.sample(n=min(100000, len(df)), random_state=42)
        sample.to_csv('data/processed/sample_orders.csv', index=False)
        print("Sample dataset created for testing!")

    except Exception as e:
        print(f"\nError preparing dataset: {str(e)}")

if __name__ == "__main__":
    main() 