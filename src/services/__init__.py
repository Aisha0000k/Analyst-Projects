"""
Business logic services for the analyst dashboard.
Contains data transformation and business rules.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from diskcache import Cache
from ..data import SupabaseClient, APIClient
from ..models import DashboardMetric


class DataPipelineService:
    """
    I am a service for ETL (Extract, Transform, Load) operations.
    I handle data collection, cleaning, and preparation from various sources.
    """

    def __init__(
        self, db_client: SupabaseClient, api_client: Optional[APIClient] = None
    ):
        """
        I initialize the data pipeline service with database and optional API clients.

        Args:
            db_client: Database client instance.
            api_client: Optional API client for external data.
        """
        self.db = db_client
        self.api = api_client

    def extract_from_database(self, query: str) -> pd.DataFrame:
        """
        I extract data from the database using a SQL query.

        Args:
            query: SQL query to execute.

        Returns:
            pd.DataFrame: Extracted data.
        """
        return self.db.execute_query(query)

    def extract_from_api(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> pd.DataFrame:
        """
        I extract data from an external API.

        Args:
            endpoint: API endpoint to call.
            params: Optional query parameters.

        Returns:
            pd.DataFrame: Extracted data.
        """
        if self.api is None:
            raise ValueError("API client not initialized")
        return self.api.get_dataframe(endpoint, params=params)

    def transform_data(
        self, df: pd.DataFrame, transformation_rules: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        I apply transformation rules to the data.

        Args:
            df: Input DataFrame.
            transformation_rules: Dictionary of transformation rules.

        Returns:
            pd.DataFrame: Transformed data.
        """
        processed_df = df.copy()
        
        # Example transformation: handle missing values
        if "fillna" in transformation_rules:
            processed_df = processed_df.fillna(transformation_rules["fillna"])
            
        # Example transformation: drop columns
        if "drop_columns" in transformation_rules:
            processed_df = processed_df.drop(columns=transformation_rules["drop_columns"])
            
        # Example transformation: rename columns
        if "rename_columns" in transformation_rules:
            processed_df = processed_df.rename(columns=transformation_rules["rename_columns"])
            
        return processed_df

    def aggregate_metrics(
        self, df: pd.DataFrame, group_by: List[str], aggregations: Dict[str, str]
    ) -> pd.DataFrame:
        """
        I aggregate data by specified columns and functions.

        Args:
            df: Input DataFrame.
            group_by: Columns to group by.
            aggregations: Dict of column -> aggregation function.

        Returns:
            pd.DataFrame: Aggregated data.
        """
        return df.groupby(group_by).agg(aggregations).reset_index()

    def load_to_database(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "append"
    ) -> Dict[str, Any]:
        """
        I load the data into the database.

        Args:
            df: DataFrame to load.
            table_name: Target table name.
            if_exists: How to behave if table exists ('append', 'replace', 'fail').

        Returns:
            Dict: Load result details.
        """
        if if_exists == "append":
            return self.db.insert_data(table_name, df)
        elif if_exists == "replace":
            # For simplicity, we just upsert if replace is requested
            # In a real scenario, we might want to truncate first
            return self.db.upsert_data(table_name, df, match_columns=[])
        else:
            return {"status": "error", "message": f"Unsupported mode: {if_exists}"}


class DashboardService:
    """
    I am a service for managing dashboard metrics and KPIs.
    """

    def __init__(self, db_client: SupabaseClient):
        """
        I initialize the dashboard service with a database client.

        Args:
            db_client: Database client instance.
        """
        self.db = db_client

    def get_metrics(self, metric_names: List[str]) -> List[DashboardMetric]:
        """
        I retrieve dashboard metrics from the database.

        Args:
            metric_names: List of metric names to retrieve.

        Returns:
            List[DashboardMetric]: Retrieved metrics.
        """
        # Placeholder for actual metric retrieval from a metrics table
        metrics = []
        for name in metric_names:
            metrics.append(DashboardMetric(name=name, value=0))
        return metrics

    def calculate_kpis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        I calculate key performance indicators from the provided data.

        Args:
            df: Input DataFrame.

        Returns:
            Dict: Calculated KPIs.
        """
        kpis = {}
        if "Outcome" in df.columns:
            # Assume Outcome 1 is success, 0 is failure
            success_rate = df["Outcome"].mean() * 100
            kpis["success_rate"] = f"{success_rate:.1f}%"
            kpis["total_launches"] = len(df)
            kpis["successful_landings"] = df["Outcome"].sum()
        
        if "PayloadMass" in df.columns:
            kpis["avg_payload_mass"] = f"{df['PayloadMass'].mean():.1f} kg"
            kpis["total_payload_mass"] = f"{df['PayloadMass'].sum():.1f} kg"
            
        return kpis

    def get_trends(self, metric_name: str, period: str = "7d") -> pd.DataFrame:
        """
        I return trend data for a specific metric over a period.

        Args:
            metric_name: Name of the metric.
            period: Time period for trends ('7d', '30d', '90d', '1y').

        Returns:
            pd.DataFrame: Trend data points.
        """
        # Placeholder for trend calculation
        days = 7
        if period == "30d": days = 30
        elif period == "90d": days = 90
        elif period == "1y": days = 365
        
        dates = [datetime.now() - timedelta(days=x) for x in range(days)]
        values = np.random.randint(0, 100, size=days)
        
        return pd.DataFrame({"date": dates, "value": values}).sort_values("date")

    def export_snapshot(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        I export a current snapshot of the dashboard data.

        Args:
            filters: Optional data filters.

        Returns:
            pd.DataFrame: Dashboard snapshot data.
        """
        return pd.DataFrame()


class CacheService:
    """
    I am a service for caching data to improve application performance.
    I use diskcache for persistent storage.
    """

    def __init__(self, cache_dir: str):
        """
        I initialize the cache service with a directory for storage.

        Args:
            cache_dir: Directory for cache storage.
        """
        self.cache = Cache(cache_dir)

    def get(self, key: str) -> Optional[pd.DataFrame]:
        """
        I retrieve cached data for a given key.

        Args:
            key: Cache key.

        Returns:
            Optional[pd.DataFrame]: Cached data or None.
        """
        return self.cache.get(key)

    def set(self, key: str, data: pd.DataFrame, ttl: Optional[int] = None) -> None:
        """
        I store a DataFrame in the cache.

        Args:
            key: Cache key.
            data: Data to cache.
            ttl: Time to live in seconds (None for no expiry).
        """
        self.cache.set(key, data, expire=ttl)

    def invalidate(self, key: str) -> None:
        """
        I remove specific data from the cache.

        Args:
            key: Cache key to invalidate.
        """
        self.cache.delete(key)

    def clear_all(self) -> None:
        """
        I clear all data from the cache.
        """
        self.cache.clear()
