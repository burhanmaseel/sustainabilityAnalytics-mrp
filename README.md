# Sustainability Analytics - MRP

A comprehensive Python-based sustainability analytics platform for monitoring and analyzing renewable energy systems, grid metrics, and weather data. This project integrates multiple data sources to provide real-time insights into photovoltaic solar systems, battery storage, grid performance, and weather conditions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Streamlit Dashboard](#running-the-streamlit-dashboard)
  - [Jupyter Notebooks](#jupyter-notebooks)
- [Project Structure](#project-structure)
- [Development](#development)
- [Models and Analytics](#models-and-analytics)

## Overview

This project provides a comprehensive analytics platform for sustainability monitoring, featuring:

- **Multi-source data integration**: Enphase solar systems, Studer battery inverter systems, OpenWeather data
- **Interactive dashboards**: Real-time visualization and analysis tools
- **Advanced modeling**: Statistical, machine learning, and deep learning approaches
- **Grid monitoring**: Power quality metrics, voltage/frequency analysis, import/export tracking
- **Weather analytics**: Temperature, humidity, visibility, cloud coverage analysis
- **Time series forecasting**: LSTM, GRU, and Transformer models for energy prediction

## Features

### Interactive Dashboards
- **Enphase Dashboard**: Solar energy production, consumption, and grid interaction analysis
- **Grid Metrics Dashboard**: Voltage, frequency, battery state monitoring, and power quality analysis
- **Weather Dashboard**: Comprehensive weather data visualization and trend analysis

### Energy System Monitoring
- Real-time solar energy production tracking
- Battery state of charge and performance monitoring
- Grid import/export analysis
- Power quality metrics (voltage, frequency, harmonics)

### Weather Analytics
- Temperature and humidity tracking
- Cloud coverage and visibility analysis
- Weather condition categorization
- Correlation analysis with energy production

### Advanced Analytics
- Statistical modeling and time series analysis
- Machine learning models (XGBoost, Random Forest)
- Deep learning models (LSTM, GRU, Transformer networks)
- Feature engineering and data preprocessing

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
├── src/                    # Source code
│   ├── config/            # Configuration constants
│   ├── utils/             # Utility functions and data processing
│   └── visualization/     # Dashboard and visualization components
├── data/                  # Data storage
│   ├── sample/           # Sample datasets
│   └── processed/        # Processed data files
├── notebooks/            # Jupyter notebooks for analysis
└── requirements.txt      # Python dependencies
```

## Data Sources

### Enphase Energy Systems
- **Format**: 15-minute interval CSV data
- **Metrics**: Energy production, consumption, grid import/export
- **Period**: January 2023 - September 2024

### Studer Battery/Inverter Systems
- **Format**: Per minute CSV data
- **Metrics**: Battery voltage/current, grid voltage/frequency, power output, battery temperature
- **Period**: September 2023 - July 2024

### OpenWeather Data
- **Format**: Hourly weather observations CSV data
- **Metrics**: Temperature, humidity, pressure, visibility, cloud coverage
- **Period**: January 2023 - September 2024

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sustainabilityAnalytics-mrp
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

The project uses the following major libraries:
- **Data Analysis**: pandas, numpy, scipy
- **Visualization**: matplotlib, seaborn, plotly, streamlit
- **Machine Learning**: scikit-learn, xgboost
- **Deep Learning**: tensorflow
- **Time Series**: statsmodels
- **Solar Analytics**: pvlib

## Usage

### Running the Streamlit Dashboard

1. **Navigate to the project directory**
   ```bash
   cd sustainabilityAnalytics-mrp
   ```

2. **Launch the dashboard**
   ```bash
   streamlit run src/visualization/home.py
   ```

3. **Access the dashboard**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - Select a dashboard from the sidebar

### Dashboards

#### Home Dashboard
- Project overview and navigation
- Quick access to all analysis tools

#### Enphase Dashboard
- Interactive energy production/consumption visualizations
- Time series analysis with matplotlib
- Energy balance calculations
- Daily and hourly pattern analysis
- Statistical summaries and correlations

#### Grid Metrics Dashboard
- Real-time grid performance monitoring
- Voltage and frequency analysis across multiple phases
- Battery state of charge tracking
- Grid connection status monitoring
- Power import/export analysis
- Interactive date range selection

#### Weather Dashboard
- Comprehensive weather data visualization
- Temperature and humidity trends
- Visibility and cloud coverage analysis
- Weather condition categorization
- Dew point calculations

### Jupyter Notebooks

The project includes comprehensive Jupyter notebooks for detailed analysis:

1. **Data Exploration** (`01_data_exploration.ipynb`)
   - Initial data investigation
   - Data quality assessment
   - Basic statistical analysis

2. **Data Preprocessing** (`02_data_preprocessing.ipynb`)
   - Data cleaning and validation
   - Missing value handling
   - Data normalization and resampling

3. **Feature Engineering** (`03_feature_engineering.ipynb`)
   - Advanced feature creation
   - Time-based feature extraction
   - Correlation analysis

4. **Statistical Modeling** (`04_modeling_statistical.ipynb`)
   - Time series decomposition
   - ARIMA and seasonal modeling
   - Statistical forecasting

5. **Machine Learning** (`05_modeling_ml.ipynb`)
   - XGBoost, Random Forest implementations
   - Model evaluation and comparison
   - Feature importance analysis

6. **Deep Learning** (`06_modeling_dl.ipynb`)
   - LSTM, GRU, and Transformer models
   - Advanced neural network architectures
   - Model performance evaluation

## Project Structure

```
sustainabilityAnalytics-mrp/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── LICENSE                      # License information
│
├── data/                        # Data directory
│   ├── sample/                  # Sample datasets
│   │   ├── enphase/            # Enphase energy data
│   │   ├── studer/             # Studer battery/inverter data
│   │   └── weather/            # Weather data files
│   └── processed/              # Processed data outputs
│
├── notebooks/                   # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling_statistical.ipynb
│   ├── 05_modeling_ml.ipynb
│   └── 06_modeling_dl.ipynb
│
└── src/                         # Source code
    ├── __init__.py
    ├── config/                  # Configuration files
    │   ├── __init__.py
    │   ├── openweather_weather_constants.py
    │   ├── pq_parameter_constants.py
    │   └── studer_constants.py
    │
    ├── utils/                   # Utility modules
    │   ├── __init__.py
    │   ├── data_processing.py          # Data processing utilities
    │   ├── data_reader.py              # Data reading functions
    │   ├── feature_engineering.py      # Feature engineering tools
    │   ├── grid_metrics_helpers.py     # Grid analysis helpers
    │   ├── pq_metrics_helpers.py       # Power quality metrics
    │   ├── streamlit_visualization_helpers.py
    │   ├── studer_data_helpers.py      # Studer data processing
    │   └── weather_helpers.py          # Weather data utilities
    │
    └── visualization/           # Dashboard components
        ├── __init__.py
        ├── home.py                     # Main dashboard entry point
        ├── enphase_dashboard.py        # Solar energy dashboard
        ├── grid_metrics_dashboard.py   # Grid monitoring dashboard
        ├── weather_dashboard_open_weather.py
        │
        ├── open_weather/        # Weather visualization modules
        │   ├── clouds_visualization.py
        │   ├── dew_point_visualization.py
        │   ├── temperature_visualization.py
        │   ├── visibility_visualization.py
        │   └── weather_conditions_visualization.py
        │
        └── studer/             # Studer system visualizations
            ├── battery_soc_visualization.py
            ├── frequency_visualization.py
            ├── grid_connection_visualization.py
            ├── grid_impex_visualization.py
            └── voltage_visualization.py
```

## Development

### Code Structure

- **Modular Design**: Clear separation between data processing, analysis, and visualization
- **Configuration Management**: Centralized constants and parameters
- **Utility Functions**: Reusable data processing and analysis tools
- **Interactive Visualizations**: Streamlit-based dashboards with real-time capabilities

### Data Processing Pipeline

1. **Data Ingestion**: Automated reading of CSV files from multiple sources
2. **Data Cleaning**: Missing value handling, outlier detection, data validation
3. **Feature Engineering**: Time-based features, rolling statistics, derived metrics
4. **Model Training**: Statistical, ML, and DL model implementations
5. **Visualization**: Interactive dashboards and static plot generation

## Models and Analytics

### Statistical Models
- ARIMA
- Exponential smoothing
- Trend and seasonality analysis

### Machine Learning Models
- **XGBoost**: Gradient boosting for energy prediction
- **Random Forest**: Ensemble methods for robust forecasting
- **Support Vector Machines**: Non-linear pattern recognition

### Deep Learning Models
- **LSTM Networks**: Long short-term memory for sequence prediction
- **GRU Networks**: Gated recurrent units for time series forecasting
- **Transformer Models**: Attention-based architectures for complex temporal patterns

### Evaluation Metrics
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R-squared (R²)
- Symmetric Mean Absolute Percentage Error (SMAPE)
