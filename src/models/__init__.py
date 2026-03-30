"""
Data models and schemas for the analyst dashboard.
Defines data structures used across the application.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd


@dataclass
class DataSource:
    """
    I represent a data source configuration.
    """

    name: str
    source_type: str
    connection_params: Dict[str, Any]
    refresh_interval: Optional[int] = None


@dataclass
class DashboardMetric:
    """
    I represent a single metric displayed on the dashboard.
    """

    name: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[float] = None
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class QueryResult:
    """
    I am a container for database query results.
    """

    data: pd.DataFrame
    query: str
    execution_time: float
    row_count: int
    timestamp: datetime = field(default_factory=datetime.now)

    def is_empty(self) -> bool:
        """I check if the query returned any results."""
        return self.data.empty

    def to_csv(self, path: str) -> None:
        """I export the results to a CSV file."""
        self.data.to_csv(path, index=False)

    def to_json(self, path: str) -> None:
        """I export the results to a JSON file."""
        self.data.to_json(path, orient="records", indent=2)


class DataSchema:
    """
    I define schemas for data validation and transformation.
    """

    _schemas = {
        "spacex_launches": [
            "FlightNumber", "Date", "BoosterVersion", "PayloadMass",
            "Orbit", "LaunchSite", "Outcome", "Flights", "GridFins",
            "Reused", "Legs", "LandingPad", "Block", "ReusedCount",
            "Serial", "Longitude", "Latitude"
        ]
    }

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, schema_name: str) -> bool:
        """
        I validate a DataFrame against a known schema.

        Args:
            df: DataFrame to validate.
            schema_name: Name of the schema to validate against.

        Returns:
            bool: True if valid, False otherwise.
        """
        expected = DataSchema.get_expected_columns(schema_name)
        return all(col in df.columns for col in expected)

    @staticmethod
    def get_expected_columns(schema_name: str) -> List[str]:
        """
        I return the expected column names for a given schema.

        Args:
            schema_name: Name of the schema.

        Returns:
            List[str]: List of expected column names.
        """
        return DataSchema._schemas.get(schema_name, [])
