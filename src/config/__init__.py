"""
Configuration module for analyst dashboard.
Handles environment variables and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class SupabaseConfig:
    """
    Configuration container for Supabase connection settings.
    """

    url: str
    key: str
    timeout: int = 30


class Config:
    """
    Main configuration class that loads and validates environment variables.
    Ensures idempotent initialization - safe to call multiple times.
    """

    _instance: Optional["Config"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize configuration from environment variables.
        Only initializes once due to idempotent design.
        """
        if self._initialized:
            return

        self.project_root = Path(__file__).parent.parent.parent
        self.env_path = self.project_root / ".env"

        self._load_env_file()
        self._validate_config()

        Config._initialized = True

    def _load_env_file(self) -> None:
        """
        Load environment variables from .env file if it exists.
        Idempotent - no action if file doesn't exist.
        """
        pass

    def _validate_config(self) -> None:
        """
        Validate that required configuration values are present.
        Raises appropriate errors for missing configuration.
        """
        pass

    @property
    def supabase(self) -> SupabaseConfig:
        """
        Get Supabase configuration.

        Returns:
            SupabaseConfig: Configured Supabase settings.
        """
        pass

    @property
    def data_dir(self) -> Path:
        """
        Get the data directory path for storing cached data.

        Returns:
            Path: Path to data directory.
        """
        pass

    @property
    def dashboard_dir(self) -> Path:
        """
        Get the dashboards directory path.

        Returns:
            Path: Path to dashboards directory.
        """
        pass


def get_config() -> Config:
    """
    Get singleton configuration instance.

    Returns:
        Config: Application configuration.
    """
    pass
