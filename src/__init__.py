"""
Analyst Dashboard - Main Application Entry Point.

This module provides the main application interface for the analyst dashboard.
It initializes all services and provides methods for running the dashboard.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .config import Config, get_config
from .data import (
    SupabaseClient,
    create_supabase_client,
    APIClient,
    AuthenticatedAPIClient,
)
from .services import DataPipelineService, DashboardService, CacheService
from .models import DashboardMetric, QueryResult, DataSource


class AnalystDashboard:
    """
    I am the main application class for the Analyst Dashboard.
    I provide a unified interface for all dashboard operations and services.
    """

    def __init__(self, config: Optional[Config] = None):
        """
        I initialize the Analyst Dashboard with a configuration instance.

        Args:
            config: Optional Config instance. If not provided, loads from environment.
        """
        self.config = config or get_config()
        self._db: Optional[SupabaseClient] = None
        self._api: Optional[APIClient] = None
        self._pipeline: Optional[DataPipelineService] = None
        self._dashboard: Optional[DashboardService] = None
        self._cache: Optional[CacheService] = None
        self._initialized = False

    def initialize(self) -> None:
        """
        I initialize all dashboard components and services.
        I ensure this is idempotent and safe to call multiple times.
        """
        if self._initialized:
            return

        self._db = create_supabase_client()
        self._api = APIClient(base_url="https://api.spacexdata.com/v4")
        self._pipeline = DataPipelineService(self._db, self._api)
        self._dashboard = DashboardService(self._db)
        self._cache = CacheService(str(self.config.data_dir / "cache"))
        
        self._initialized = True

    def connect_database(self) -> None:
        """
        I establish the database connection.
        """
        if not self._initialized:
            self.initialize()
        if self._db:
            self._db.connect()

    def disconnect(self) -> None:
        """
        I disconnect all connections and cleanup resources.
        """
        if self._db:
            self._db.disconnect()
        if self._cache:
             self._cache.clear_all()

    def run(self, dashboard_type: str = "cli") -> None:
        """
        I run the dashboard application based on the specified type.

        Args:
            dashboard_type: Type of dashboard to run ('cli', 'streamlit', 'panel').
        """
        if not self._initialized:
            self.initialize()

        if dashboard_type == "cli":
            self.run_cli()
        elif dashboard_type == "streamlit":
            self.run_streamlit()
        elif dashboard_type == "panel":
            self.run_panel()
        else:
            print(f"Error: Unknown dashboard type '{dashboard_type}'")

    def run_cli(self) -> None:
        """
        I run the dashboard in command-line interface mode.
        """
        print("Starting Analyst Dashboard in CLI mode...")
        # Simple CLI display of KPIs
        # In a real app, this would fetch data from the pipeline/dashboard service
        print("Success Rate: 89%")
        print("Total Launches: 90")

    def run_streamlit(self, port: int = 8501) -> None:
        """
        I run the dashboard with a Streamlit web interface.

        Args:
            port: Port number for the web server.
        """
        print(f"Starting Streamlit dashboard on port {port}...")
        # In a real app, this would call 'streamlit run' on a script
        pass

    def run_panel(self, port: int = 5006) -> None:
        """
        I run the dashboard with a Panel web interface.

        Args:
            port: Port number for the web server.
        """
        print(f"Starting Panel dashboard on port {port}...")
        # In a real app, this would start the Panel server
        pass

    @property
    def pipeline(self) -> DataPipelineService:
        """
        I provide access to the data pipeline service.

        Returns:
            DataPipelineService: Pipeline service instance.
        """
        if not self._initialized: self.initialize()
        return self._pipeline

    @property
    def dashboard(self) -> DashboardService:
        """
        I provide access to the dashboard service.

        Returns:
            DashboardService: Dashboard service instance.
        """
        if not self._initialized: self.initialize()
        return self._dashboard

    @property
    def cache(self) -> CacheService:
        """
        I provide access to the cache service.

        Returns:
            CacheService: Cache service instance.
        """
        if not self._initialized: self.initialize()
        return self._cache


def create_app() -> AnalystDashboard:
    """
    I am a factory function to create a new dashboard application instance.

    Returns:
        AnalystDashboard: New dashboard instance.
    """
    return AnalystDashboard()


def main() -> None:
    """
    I am the main entry point for the dashboard application.
    I parse command-line arguments and run the requested dashboard type.
    """
    parser = argparse.ArgumentParser(description="SpaceX Falcon 9 Analyst Dashboard")
    parser.add_argument("--streamlit", action="store_true", help="Run Streamlit dashboard")
    parser.add_argument("--panel", action="store_true", help="Run Panel dashboard")
    parser.add_argument("--port", type=int, default=None, help="Port number for web server")
    
    args = parser.parse_args()
    
    app = create_app()
    
    if args.streamlit:
        app.run("streamlit")
    elif args.panel:
        app.run("panel")
    else:
        app.run("cli")


if __name__ == "__main__":
    main()
