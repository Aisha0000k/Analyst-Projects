"""
Data models and schemas for the analyst dashboard.
Defines data structures used across the application.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd


@dataclass
class DataSource:
    """
    Represents a data source configuration.
    """

    name: str
    source_type: str
    connection_params: Dict[str, Any]
    refresh_interval: Optional[int] = None


@dataclass
class DashboardMetric:
    """
    Represents a single metric displayed on the dashboard.
    """

    name: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[float] = None
    last_updated: Optional[datetime] = None


@dataclass
class QueryResult:
    """
    Container for database query results.
    """

    data: pd.DataFrame
    query: str
    execution_time: float
    row_count: int
    timestamp: datetime

    def is_empty(self) -> bool:
        """Check if query returned any results."""
        pass

    def to_csv(self, path: str) -> None:
        """Export results to CSV file."""
        pass

    def to_json(self, path: str) -> None:
        """Export results to JSON file."""
        pass


class DataSchema:
    """
    Schema definitions for data validation and transformation.
    """

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, schema_name: str) -> bool:
        """
        Validate a DataFrame against a known schema.

        Args:
            df: DataFrame to validate.
            schema_name: Name of the schema to validate against.

        Returns:
            bool: True if valid, False otherwise.
        """
        pass

    @staticmethod
    def get_expected_columns(schema_name: str) -> List[str]:
        """
        Get expected column names for a schema.

        Args:
            schema_name: Name of the schema.

        Returns:
            List[str]: List of expected column names.
        """
        pass
