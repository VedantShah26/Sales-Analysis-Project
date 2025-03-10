# Sales Analysis Project

A comprehensive sales analysis project that includes data processing, analysis, and visualization using Python. The project features a Streamlit dashboard for interactive data exploration and insights.

## Features

- Data processing and analysis pipeline
- Interactive Streamlit dashboard
- Sales trend analysis
- Product performance metrics
- Customer behavior insights
- Automated report generation

## Project Structure

```
sales-analysis-project/
├── data/
│   ├── raw/           # Raw data files
│   └── processed/     # Processed data files
├── src/
│   ├── data/         # Data processing scripts
│   └── analysis/     # Analysis scripts
├── dashboard/        # Streamlit dashboard
├── notebooks/        # Jupyter notebooks
├── reports/         # Generated reports and visualizations
├── tests/           # Unit tests
└── config/          # Configuration files
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sales-analysis-project.git
cd sales-analysis-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Generate sample data (if using sample data):
```bash
python src/data/generate_sample_data.py
```

2. Run the analysis:
```bash
python src/analysis/sales_analysis.py
```

3. Launch the dashboard:
```bash
streamlit run dashboard/app.py
```

## Project Components

### Data Processing
- `src/data/generate_sample_data.py`: Generates sample sales data for testing
- `src/data/download_data.py`: Downloads and processes raw data

### Analysis
- `src/analysis/sales_analysis.py`: Main analysis script with the `SalesAnalyzer` class
- `notebooks/01_exploratory_analysis.ipynb`: Jupyter notebook for exploratory data analysis

### Dashboard
- `dashboard/app.py`: Streamlit dashboard for interactive data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python, Pandas, and Streamlit
- Uses Plotly for interactive visualizations
- Inspired by real-world sales analysis needs 