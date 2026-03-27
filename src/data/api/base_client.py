"""
Generic REST API client for external data sources.
Provides methods for GET, POST, PUT, DELETE operations.
"""

import pandas as pd
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin


class APIClient:
    """
    Generic HTTP client for REST APIs.
    Handles authentication, request/response processing.
    """

    def __init__(
        self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30
    ):
        """
        Initialize API client.

        Args:
            base_url: Base URL for API endpoints.
            headers: Optional default headers.
            timeout: Request timeout in seconds.
        """
        pass

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform GET request.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            Dict: Response data.
        """
        pass

    def post(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Perform POST request.

        Args:
            endpoint: API endpoint path.
            data: Form data.
            json: JSON body data.

        Returns:
            Dict: Response data.
        """
        pass

    def put(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Perform PUT request.

        Args:
            endpoint: API endpoint path.
            data: Form data.
            json: JSON body data.

        Returns:
            Dict: Response data.
        """
        pass

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform DELETE request.

        Args:
            endpoint: API endpoint path.

        Returns:
            Dict: Response data.
        """
        pass

    def get_dataframe(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> pd.DataFrame:
        """
        Fetch data and convert to DataFrame.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            pd.DataFrame: Response data as DataFrame.
        """
        pass

    def paginate(
        self, endpoint: str, page_param: str = "page", max_pages: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch paginated data and combine into single DataFrame.

        Args:
            endpoint: API endpoint path.
            page_param: Name of pagination parameter.
            max_pages: Maximum pages to fetch (None for all).

        Returns:
            pd.DataFrame: Combined paginated data.
        """
        pass


class AuthenticatedAPIClient(APIClient):
    """
    API client with authentication support.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ):
        """
        Initialize authenticated API client.

        Args:
            base_url: Base URL for API endpoints.
            api_key: API key for authentication.
            headers: Optional default headers.
            timeout: Request timeout in seconds.
        """
        pass

    def refresh_token(self) -> None:
        """
        Refresh authentication token if expired.
        """
        pass

    def set_auth_header(self, token: str) -> None:
        """
        Set authorization header manually.

        Args:
            token: Authentication token.
        """
        pass
