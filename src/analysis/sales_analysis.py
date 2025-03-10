import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

class SalesAnalyzer:
    def __init__(self, data_path):
        """Initialize the SalesAnalyzer with data path."""
        self.data_path = Path(data_path)
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load and prepare the sales data."""
        try:
            # Load the data
            self.data = pd.read_csv(self.data_path)
            
            # Convert date columns to datetime
            date_columns = self.data.select_dtypes(include=['object']).columns
            for col in date_columns:
                if 'date' in col.lower():
                    self.data[col] = pd.to_datetime(self.data[col])
            
            print(f"Data loaded successfully. Shape: {self.data.shape}")
            print("\nColumns in the dataset:")
            print(self.data.columns.tolist())
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
    
    def get_basic_stats(self):
        """Get basic statistics about the sales data."""
        if self.data is None:
            return "No data loaded"
        
        stats = {
            'Total Sales': self.data['sales'].sum(),
            'Average Sale': self.data['sales'].mean(),
            'Total Orders': len(self.data),
            'Unique Products': self.data['product_id'].nunique(),
            'Unique Customers': self.data['customer_id'].nunique(),
            'Date Range': f"{self.data['order_date'].min().date()} to {self.data['order_date'].max().date()}"
        }
        
        return pd.Series(stats)
    
    def analyze_sales_trends(self):
        """Analyze sales trends over time."""
        if self.data is None:
            return None
        
        # Daily sales
        daily_sales = self.data.groupby('order_date')['sales'].sum().reset_index()
        
        # Create a line plot
        fig = px.line(daily_sales, x='order_date', y='sales',
                     title='Daily Sales Trend',
                     labels={'order_date': 'Date', 'sales': 'Sales Amount'})
        
        return fig
    
    def analyze_product_performance(self):
        """Analyze product performance."""
        if self.data is None:
            return None
        
        # Top products by sales
        product_performance = self.data.groupby('product_id').agg({
            'sales': ['sum', 'count', 'mean'],
            'product_name': 'first'
        }).reset_index()
        
        product_performance.columns = ['product_id', 'total_sales', 'orders', 'avg_sale', 'product_name']
        product_performance = product_performance.sort_values('total_sales', ascending=False)
        
        # Create a bar plot for top 10 products
        fig = px.bar(product_performance.head(10),
                    x='product_name', y='total_sales',
                    title='Top 10 Products by Sales',
                    labels={'product_name': 'Product', 'total_sales': 'Total Sales'})
        
        return fig, product_performance
    
    def analyze_customer_behavior(self):
        """Analyze customer purchasing behavior."""
        if self.data is None:
            return None
        
        # Customer purchase frequency
        customer_stats = self.data.groupby('customer_id').agg({
            'order_id': 'count',
            'sales': ['sum', 'mean']
        }).reset_index()
        
        customer_stats.columns = ['customer_id', 'total_orders', 'total_spent', 'avg_order_value']
        
        # Create a scatter plot of orders vs total spent
        fig = px.scatter(customer_stats,
                        x='total_orders', y='total_spent',
                        title='Customer Purchase Behavior',
                        labels={'total_orders': 'Number of Orders',
                               'total_spent': 'Total Amount Spent'})
        
        return fig, customer_stats
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        if self.data is None:
            return "No data loaded"
        
        report = {
            'Basic Statistics': self.get_basic_stats(),
            'Sales Trends': self.analyze_sales_trends(),
            'Product Performance': self.analyze_product_performance(),
            'Customer Behavior': self.analyze_customer_behavior()
        }
        
        return report

def main():
    # Initialize the analyzer
    data_path = Path("data/processed/merged_orders.csv")
    analyzer = SalesAnalyzer(data_path)
    
    # Generate and display the summary report
    report = analyzer.generate_summary_report()
    
    # Save visualizations
    output_dir = Path("reports/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save sales trends
    if report['Sales Trends']:
        report['Sales Trends'].write_html(output_dir / "sales_trends.html")
    
    # Save product performance
    if report['Product Performance']:
        fig, _ = report['Product Performance']
        fig.write_html(output_dir / "product_performance.html")
    
    # Save customer behavior
    if report['Customer Behavior']:
        fig, _ = report['Customer Behavior']
        fig.write_html(output_dir / "customer_behavior.html")
    
    print("\nAnalysis complete! Check the reports/figures directory for visualizations.")

if __name__ == "__main__":
    main() 