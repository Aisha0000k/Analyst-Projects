# SpaceX Falcon 9 Analyst Dashboard

Idempotent data pipeline that collects, transforms, and analyzes SpaceX Falcon 9 launch data from multiple sources, producing an analyst dashboard with Supabase integration and dynamic visualizations (Tableau, Plotly, Panel, Streamlit).

## Data Pipeline Overview

This project implements an idempotent ETL pipeline that aggregates SpaceX Falcon 9 launch data from multiple sources:

| Source | Module | Description |
|--------|--------|-------------|
| SpaceX API | `spacex_data_collection.py` | REST API collection with pagination and rate limiting |
| Wikipedia | `spacex_web_scraping.py` | Web scraping for Falcon 9 launch records |
| CSV Files | `spacex_data_wrangling.py` | Local data loading and preprocessing |
| SQLite Database | `spacex_sql_analysis.py` | SQL queries for exploratory analysis |
| Feature Engineering | `spacex_data_wrangling.py` | Label generation and class balancing |

## Modules

| Module | Purpose |
|--------|---------|
| `spacex_data_collection.py` | Collects launch data from SpaceX REST API with automatic pagination |
| `spacex_web_scraping.py` | Scrapes Falcon 9 launch records from Wikipedia tables |
| `spacex_data_wrangling.py` | Cleans data, handles missing values, generates success/failure labels |
| `spacex_eda_visualization.py` | Exploratory data analysis with matplotlib/seaborn visualizations |
| `spacex_launch_site_location.py` | Geospatial analysis with Folium maps showing launch sites |
| `spacex_sql_analysis.py` | SQL queries for filtering, aggregation, and trend analysis |
| `spacex_ml_prediction.py` | Machine learning models for launch outcome prediction |

### Pipeline Stages

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Data Wrangling │───▶│  EDA & Analysis │
│  (API, Web, CSV)│    │  (Clean, Label) │    │  (SQL, Charts)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Dashboard      │◀───│  Visualization  │◀───│  ML Prediction  │
│  (Supabase)     │    │  (Plotly, Folium│    │  (Classification│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Features

### Data Layer
- **Supabase Integration**: Connect to Supabase database for data storage and retrieval
- **REST API Client**: Generic HTTP client for external data sources with pandas DataFrame output
- **Authenticated API Client**: API client with token-based authentication support
- **Pagination Support**: Automatic handling of paginated API responses

### Business Logic (Services)
- **DataPipelineService**: ETL operations - Extract, Transform, Load data from multiple sources
- **DashboardService**: KPIs calculation, metrics retrieval, trend analysis
- **CacheService**: Local caching to improve performance

### Machine Learning
Built an ML classification pipeline achieving 89% accuracy in predicting Falcon 9 first-stage landing outcomes using Logistic Regression with 8 engineered features, enabling actionable launch success forecasting for stakeholder decision-making.

### Visualization
- **Tableau Integration**: Connect to Tableau Server, extract data from views, build dashboards programmatically
- **PlotlyDashboard**: Interactive charts (line, bar, scatter, heatmap) exported to HTML
- **PanelDashboard**: Dynamic dashboards with widgets and real-time updates
- **StreamlitDashboard**: Web-based dashboards with metrics, charts, and filters

### Architecture
- **Idempotent Design**: Safe to run multiple times without side effects
- **Singleton Configuration**: Single Config instance across the application
- **Data Models**: Schema validation and transformation utilities

## Directory Structure

```
Analyst-Projects/
├── spacex_data_collection.py     # SpaceX API data collection
├── spacex_web_scraping.py        # Wikipedia web scraping
├── spacex_data_wrangling.py      # Data cleaning and labeling
├── spacex_eda_visualization.py    # Exploratory data analysis
├── spacex_launch_site_location.py # Geospatial analysis with Folium
├── spacex_sql_analysis.py         # SQL-based analysis
├── spacex_ml_prediction.py        # ML prediction models
├── src/                          # Shared utilities
│   ├── config/
│   │   └── __init__.py          # Environment handling, singleton Config
│   ├── data/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── base_client.py   # REST API client
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── supabase.py      # Supabase client
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py          # Data schemas, validation
│   ├── services/
│   │   └── __init__.py          # Business logic layer
│   ├── visualizations/
│   │   ├── __init__.py
│   │   ├── tableau.py           # Tableau integration
│   │   └── dynamic.py           # Plotly, Panel, Streamlit
│   └── __init__.py
├── dashboards/                   # Tableau workbooks (.twb, .twbx)
├── notebooks/                     # Original Jupyter notebooks
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── .gitignore
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Open `.env` and fill in your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-or-service-key
   ```

3. **Verify Installation**
   ```bash
   python main.py
   ```

## How to Run

### CLI Mode (Default)
```bash
python main.py
```

### Streamlit Web Dashboard
```bash
python main.py --streamlit
# Opens at http://localhost:8501
```

### Panel Web Dashboard
```bash
python main.py --panel
# Opens at http://localhost:5006
```

### With Arguments
```bash
python main.py --streamlit --port 8080
```

## Usage Examples

### Run Data Collection Pipeline
```bash
# Collect data from SpaceX API
python spacex_data_collection.py

# Scrape data from Wikipedia
python spacex_web_scraping.py

# Run data wrangling and labeling
python spacex_data_wrangling.py
```

### Data Analysis
```bash
# Run EDA visualizations
python spacex_eda_visualization.py

# Analyze launch site locations
python spacex_launch_site_location.py

# Execute SQL queries
python spacex_sql_analysis.py
```

### Machine Learning
```bash
# Train prediction models
python spacex_ml_prediction.py
```

### Supabase Database Connection
```python
from src.data.database import create_supabase_client

client = create_supabase_client()
client.connect()
df = client.fetch_table("sales_data")
```

### API Data Retrieval
```python
from src.data.api import APIClient

client = APIClient(base_url="https://api.example.com")
df = client.get_dataframe("/sales", params={"date": "2024-01-01"})
```

### Data Pipeline
```python
from src.services import DataPipelineService

pipeline = DataPipelineService(db_client, api_client)
df = pipeline.extract_from_database("SELECT * FROM sales")
df = pipeline.extract_from_api("/api/metrics")
```

### Tableau Integration
```python
from src.visualizations import TableauConnector, TableauDashboardBuilder

connector = TableauConnector(server_url="https://tableau-server.com")
builder = TableauDashboardBuilder(output_dir="./dashboards")
```

### Dynamic Dashboard
```python
from src.visualizations import PlotlyDashboard, PanelDashboard, StreamlitDashboard

# Plotly
dashboard = PlotlyDashboard(title="Sales Report")
dashboard.add_line_chart("date", ["revenue", "profit"])
dashboard.save_html("report.html")

# Panel
dashboard = PanelDashboard(title="Interactive Dashboard")
dashboard.add_widget("select", "region", options=["North", "South"])
```

## Requirements

- Python 3.10+
- pandas >= 2.0.0
- numpy >= 1.24.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- folium >= 0.14.0
- sqlalchemy >= 2.0.0
- scikit-learn >= 1.3.0
- supabase >= 2.0.0
- plotly >= 5.18.0
- panel >= 1.3.0
- streamlit >= 1.30.0
- tableauserverclient >= 0.25
- python-dotenv >= 1.0.0

See `requirements.txt` for complete list.

## Extending the Pipeline

1. **Add new data sources**: Create new collection modules following the pattern in `spacex_data_collection.py`
2. **Add new transformations**: Extend `spacex_data_wrangling.py` with additional cleaning functions
3. **Add new ML models**: Extend `spacex_ml_prediction.py` with additional classifiers
4. **Add new visualizations**: Create in `src/visualizations/` or extend existing modules
5. **Add Tableau workbooks**: Place in `dashboards/` directory
