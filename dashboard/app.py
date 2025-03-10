import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.analysis.sales_analysis import SalesAnalyzer

# Set page config
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Sales Analysis Dashboard")
st.markdown("""
This dashboard provides insights into sales performance, product analysis, and customer behavior.
Use the sidebar to navigate between different sections.
""")

# Initialize the analyzer
@st.cache_data
def load_data():
    analyzer = SalesAnalyzer("data/processed/merged_orders.csv")
    return analyzer

analyzer = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a section",
    ["Overview", "Sales Trends", "Product Analysis", "Customer Insights"]
)

if page == "Overview":
    st.header("Overview")
    
    # Display basic statistics
    stats = analyzer.get_basic_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sales", f"${stats['Total Sales']:,.2f}")
        st.metric("Average Sale", f"${stats['Average Sale']:,.2f}")
    
    with col2:
        st.metric("Total Orders", f"{stats['Total Orders']:,}")
        st.metric("Unique Products", f"{stats['Unique Products']:,}")
    
    with col3:
        st.metric("Unique Customers", f"{stats['Unique Customers']:,}")
        st.metric("Date Range", stats['Date Range'])

elif page == "Sales Trends":
    st.header("Sales Trends")
    
    # Display sales trends
    fig = analyzer.analyze_sales_trends()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Add date range selector
    st.subheader("Filter by Date Range")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", analyzer.data['order_date'].min().date())
    with col2:
        end_date = st.date_input("End Date", analyzer.data['order_date'].max().date())

elif page == "Product Analysis":
    st.header("Product Analysis")
    
    # Display product performance
    fig, product_data = analyzer.analyze_product_performance()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed product table
    st.subheader("Product Performance Details")
    st.dataframe(product_data)

elif page == "Customer Insights":
    st.header("Customer Insights")
    
    # Display customer behavior
    fig, customer_data = analyzer.analyze_customer_behavior()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Display customer segments
    st.subheader("Customer Segments")
    customer_data['segment'] = pd.qcut(customer_data['total_spent'], 
                                     q=4, 
                                     labels=['Low', 'Medium', 'High', 'VIP'])
    
    segment_stats = customer_data.groupby('segment').agg({
        'customer_id': 'count',
        'total_spent': ['sum', 'mean']
    }).round(2)
    
    st.dataframe(segment_stats)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit | Data Analysis Dashboard</p>
</div>
""", unsafe_allow_html=True) 