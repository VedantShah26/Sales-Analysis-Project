# Sales Analysis and Forecasting Project

A comprehensive data analysis and machine learning project for retail sales forecasting, customer behavior analysis, and product recommendations.

## Key Features

- **Exploratory Data Analysis (EDA)**
  - Purchase pattern analysis
  - Customer behavior insights
  - Product performance metrics
  - Seasonal trends identification

- **Machine Learning Models**
  - K-means clustering for product segmentation
  - XGBoost for sales forecasting
  - Collaborative filtering for product recommendations
  - Association rule mining for basket analysis

- **Interactive Visualizations**
  - Streamlit dashboard for real-time analytics
  - Power BI reports for business insights
  - Interactive charts and graphs
  - KPI monitoring and tracking

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sales-analysis-project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Add your configurations to .env file
```

## Project Structure

```
sales-analysis-project/
├── data/                  # Raw and processed data files
├── notebooks/            # Jupyter notebooks for analysis
├── src/                  # Source code
│   ├── data/            # Data processing scripts
│   ├── models/          # ML model implementations
│   ├── visualization/   # Visualization code
│   └── utils/           # Utility functions
├── tests/               # Unit tests
├── dashboard/           # Streamlit dashboard
├── reports/            # Power BI reports and analytics
└── config/             # Configuration files

```

## Features Implementation

1. **Data Processing**
   - Data cleaning and preprocessing
   - Feature engineering
   - Time series preparation

2. **Machine Learning Models**
   - Sales forecasting using XGBoost
   - Customer segmentation using K-means
   - Product recommendation system
   - Market basket analysis

3. **Visualization and Reporting**
   - Interactive Streamlit dashboard
   - Power BI reports
   - Performance metrics visualization
   - Trend analysis charts

## Technologies Used

- Python 3.8+
- Pandas & NumPy for data manipulation
- Scikit-learn & XGBoost for machine learning
- MLflow for experiment tracking
- Plotly & Seaborn for visualization
- Streamlit for web dashboard
- Power BI for business reporting
- PostgreSQL for data storage
- SQLAlchemy for database operations

## Getting Started with Development

1. **Data Preparation**
   - Place your sales data in the `data/raw` directory
   - Run data preprocessing scripts

2. **Model Training**
   - Execute notebooks in the `notebooks` directory
   - Train models using scripts in `src/models`

3. **Dashboard Setup**
   - Configure database connection
   - Run Streamlit dashboard
   - Set up Power BI reports

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 