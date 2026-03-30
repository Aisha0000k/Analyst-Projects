"""
Supabase database connection and query utilities.
Provides methods for connecting to and querying Supabase.
"""

import pandas as pd
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from ...config import Config, get_config


class SupabaseClient:
    """
    I am a client for interacting with the Supabase database.
    I implement connection management and common query operations.
    """

    def __init__(self, config: Config):
        """
        I initialize the Supabase client with the application configuration.

        Args:
            config: Application configuration instance.
        """
        self.config = config.supabase
        self.client: Optional[Client] = None
        self._connected = False

    def connect(self) -> None:
        """
        I establish a connection to the Supabase database.
        I ensure this is idempotent and safe to call multiple times.
        """
        if self._connected and self.client is not None:
            return

        if not self.config.url or not self.config.key:
             # I skip actual connection if credentials are missing
             # to allow the application to run in limited mode.
             return

        self.client = create_client(self.config.url, self.config.key)
        self._connected = True

    def disconnect(self) -> None:
        """
        I close the connection to the Supabase database.
        I ensure this is idempotent.
        """
        self.client = None
        self._connected = False

    def execute_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        I execute a SQL query and return the results as a DataFrame.
        Note: Supabase's python client primarily uses PostgREST.
        For raw SQL, we might need a different approach or use RPCs.
        For this implementation, I'll simulate it or use RPC if available.

        Args:
            query: SQL query string.
            params: Optional query parameters.

        Returns:
            pd.DataFrame: Query results.
        """
        # Placeholder for raw SQL execution via RPC or other mechanism
        # In a real Supabase setup, you'd often use .table().select()
        # but if we need raw SQL, we'd use a postgres driver or an RPC.
        return pd.DataFrame()

    def fetch_table(
        self, table_name: str, columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        I fetch all data from a specified table.

        Args:
            table_name: Name of the table to fetch.
            columns: Optional list of columns to select.

        Returns:
            pd.DataFrame: Table data.
        """
        if not self._connected or self.client is None:
            self.connect()
        
        if self.client is None:
            return pd.DataFrame()

        query = self.client.table(table_name).select(
            ",".join(columns) if columns else "*"
        )
        response = query.execute()
        return pd.DataFrame(response.data)

    def insert_data(self, table_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """
        I insert DataFrame data into a specified table.

        Args:
            table_name: Target table name.
            data: DataFrame to insert.

        Returns:
            Dict: Insert result details.
        """
        if not self._connected or self.client is None:
            self.connect()

        if self.client is None:
            return {"status": "error", "message": "Not connected"}

        records = data.to_dict(orient="records")
        response = self.client.table(table_name).insert(records).execute()
        return {"status": "success", "data": response.data}

    def update_data(
        self, table_name: str, data: pd.DataFrame, match_column: str
    ) -> Dict[str, Any]:
        """
        I update existing records in a table.

        Args:
            table_name: Target table name.
            data: DataFrame with updated values.
            match_column: Column to match records on.

        Returns:
            Dict: Update result details.
        """
        if not self._connected or self.client is None:
            self.connect()

        if self.client is None:
            return {"status": "error", "message": "Not connected"}

        results = []
        for _, row in data.iterrows():
            record = row.to_dict()
            match_val = record.pop(match_column)
            res = self.client.table(table_name).update(record).eq(match_column, match_val).execute()
            results.append(res.data)
        
        return {"status": "success", "data": results}

    def upsert_data(
        self, table_name: str, data: pd.DataFrame, match_columns: List[str]
    ) -> Dict[str, Any]:
        """
        I upsert data - I insert or update based on matching columns.

        Args:
            table_name: Target table name.
            data: DataFrame to upsert.
            match_columns: Columns to match existing records.

        Returns:
            Dict: Upsert result details.
        """
        if not self._connected or self.client is None:
            self.connect()

        if self.client is None:
            return {"status": "error", "message": "Not connected"}

        records = data.to_dict(orient="records")
        # Supabase's upsert uses the primary key or unique constraints
        response = self.client.table(table_name).upsert(records).execute()
        return {"status": "success", "data": response.data}


def create_supabase_client() -> SupabaseClient:
    """
    I am a factory function to create a configured Supabase client.

    Returns:
        SupabaseClient: A configured client instance.
    """
    return SupabaseClient(get_config())
