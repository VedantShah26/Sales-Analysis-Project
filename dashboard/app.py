import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yaml
import joblib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Set page config
st.set_page_config(
    page_title=config['dashboard']['title'],
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    """Load processed sales data."""
    return pd.read_csv('data/processed/processed_sales_data.csv')

def load_models():
    """Load trained models."""
    models = {}
    model_dir = config['data_paths']['model_artifacts']
    
    models['xgboost'] = joblib.load(
        os.path.join(model_dir, 'xgboost_sales_forecast.joblib')
    )
    models['kmeans'] = joblib.load(
        os.path.join(model_dir, 'kmeans_customer_segments.joblib')
    )
    
    return models

def create_sales_trend(data):
    """Create sales trend visualization."""
    daily_sales = data.groupby('order_date')['total_sales'].sum().reset_index()
    
    fig = px.line(
        daily_sales,
        x='order_date',
        y='total_sales',
        title='Daily Sales Trend'
    )
    return fig

def create_product_performance(data):
    """Create product performance visualization."""
    product_sales = data.groupby('product_id').agg({
        'total_sales': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    fig = px.scatter(
        product_sales,
        x='quantity',
        y='total_sales',
        title='Product Performance',
        labels={'total_sales': 'Total Sales', 'quantity': 'Units Sold'}
    )
    return fig

def create_customer_segments(data, kmeans_model):
    """Create customer segmentation visualization."""
    features = data[['total_sales', 'quantity', 'price']]
    clusters = kmeans_model.predict(features)
    
    fig = px.scatter_3d(
        data,
        x='total_sales',
        y='quantity',
        z='price',
        color=clusters,
        title='Customer Segments'
    )
    return fig

def main():
    """Main function for the Streamlit dashboard."""
    st.title(config['dashboard']['title'])
    
    # Load data and models
    try:
        data = load_data()
        models = load_models()
        
        # Sidebar filters
        st.sidebar.header('Filters')
        
        date_range = st.sidebar.date_input(
            'Select Date Range',
            value=(
                data['order_date'].min(),
                data['order_date'].max()
            )
        )
        
        # Main dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Sales Trend')
            sales_trend = create_sales_trend(data)
            st.plotly_chart(sales_trend, use_container_width=True)
            
        with col2:
            st.subheader('Product Performance')
            product_perf = create_product_performance(data)
            st.plotly_chart(product_perf, use_container_width=True)
        
        # Customer Segmentation
        st.subheader('Customer Segmentation')
        segments = create_customer_segments(data, models['kmeans'])
        st.plotly_chart(segments, use_container_width=True)
        
        # KPIs
        st.subheader('Key Performance Indicators')
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.metric(
                'Total Sales',
                f"${data['total_sales'].sum():,.2f}"
            )
            
        with kpi2:
            st.metric(
                'Average Order Value',
                f"${data['total_sales'].mean():,.2f}"
            )
            
        with kpi3:
            st.metric(
                'Total Orders',
                f"{len(data):,}"
            )
            
        with kpi4:
            st.metric(
                'Total Products',
                f"{data['product_id'].nunique():,}"
            )
            
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

if __name__ == "__main__":
    main() 