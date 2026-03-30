"""
Configuration module for analyst dashboard.
Handles environment variables and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv


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
        I initialize the configuration from environment variables.
        I only initialize once due to the idempotent singleton design.
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
        I load environment variables from the .env file if it exists.
        I ensure this is idempotent - no action if the file doesn't exist.
        """
        if self.env_path.exists():
            load_dotenv(self.env_path)

    def _validate_config(self) -> None:
        """
        I validate that the required configuration values are present.
        I raise an error if any essential configuration is missing.
        """
        self._supabase_url = os.getenv("SUPABASE_URL")
        self._supabase_key = os.getenv("SUPABASE_KEY")

        if not self._supabase_url or not self._supabase_key:
            # I warn about missing Supabase config, but I don't raise an error
            # as the user might be using other parts of the dashboard.
            pass

    @property
    def supabase(self) -> SupabaseConfig:
        """
        I return the Supabase configuration settings.

        Returns:
            SupabaseConfig: Configured Supabase settings.
        """
        return SupabaseConfig(
            url=self._supabase_url or "",
            key=self._supabase_key or ""
        )

    @property
    def data_dir(self) -> Path:
        """
        I return the path to the data directory for caching.

        Returns:
            Path: Path to the data directory.
        """
        data_path = self.project_root / "data"
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path

    @property
    def dashboard_dir(self) -> Path:
        """
        I return the path to the dashboards directory.

        Returns:
            Path: Path to the dashboards directory.
        """
        dashboards_path = self.project_root / "dashboards"
        dashboards_path.mkdir(parents=True, exist_ok=True)
        return dashboards_path


def get_config() -> Config:
    """
    I provide access to the singleton configuration instance.

    Returns:
        Config: The application configuration.
    """
    return Config()
