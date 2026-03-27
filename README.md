# Analyst Dashboard

Idempotent analyst dashboard architecture with Supabase integration and support for dynamic visualizations including Tableau, Plotly, Panel, and Streamlit.

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
analyst-dashboard/
├── src/
│   ├── config/
│   │   └── __init__.py       # Environment handling, singleton Config
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
│   └── __init__.py              # Main AnalystDashboard class
├── dashboards/                   # Tableau workbooks (.twb, .twbx)
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables
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
- supabase >= 2.0.0
- requests >= 2.31.0
- plotly >= 5.18.0
- panel >= 1.3.0
- streamlit >= 1.30.0
- tableauserverclient >= 0.25
- python-dotenv >= 1.0.0

See `requirements.txt` for complete list.

## Extending the Dashboard

1. **Add new API sources**: Extend `APIClient` in `src/data/api/base_client.py`
2. **Add new data models**: Define schemas in `src/models/__init__.py`
3. **Add new business logic**: Implement in `src/services/__init__.py`
4. **Add new visualizations**: Create in `src/visualizations/`
5. **Add Tableau workbooks**: Place in `dashboards/` directory
