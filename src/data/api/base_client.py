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
    I am a generic HTTP client for REST APIs.
    I handle requests, responses, and common API operations.
    """

    def __init__(
        self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30
    ):
        """
        I initialize the API client with a base URL and default settings.

        Args:
            base_url: Base URL for API endpoints.
            headers: Optional default headers.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(
        self, method: str, endpoint: str, **kwargs
    ) -> requests.Response:
        """
        I perform an internal HTTP request and handle errors.
        """
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        response = self.session.request(
            method, url, timeout=self.timeout, **kwargs
        )
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        I perform a GET request and return the JSON response.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            Dict: Response data.
        """
        response = self._request("GET", endpoint, params=params)
        return response.json()

    def post(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        I perform a POST request and return the JSON response.

        Args:
            endpoint: API endpoint path.
            data: Form data.
            json: JSON body data.

        Returns:
            Dict: Response data.
        """
        response = self._request("POST", endpoint, data=data, json=json)
        return response.json()

    def put(
        self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        I perform a PUT request and return the JSON response.

        Args:
            endpoint: API endpoint path.
            data: Form data.
            json: JSON body data.

        Returns:
            Dict: Response data.
        """
        response = self._request("PUT", endpoint, data=data, json=json)
        return response.json()

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        I perform a DELETE request and return the JSON response.

        Args:
            endpoint: API endpoint path.

        Returns:
            Dict: Response data.
        """
        response = self._request("DELETE", endpoint)
        return response.json()

    def get_dataframe(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> pd.DataFrame:
        """
        I fetch data from an endpoint and convert it to a pandas DataFrame.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            pd.DataFrame: Response data as DataFrame.
        """
        data = self.get(endpoint, params=params)
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            # If it's a dict, we might need to find the data list
            # For now, let's assume it's directly convertible or contains a 'data' key
            if "data" in data and isinstance(data["data"], list):
                return pd.DataFrame(data["data"])
            return pd.DataFrame([data])
        return pd.DataFrame()

    def paginate(
        self, endpoint: str, page_param: str = "page", max_pages: Optional[int] = None
    ) -> pd.DataFrame:
        """
        I fetch paginated data and combine it into a single DataFrame.

        Args:
            endpoint: API endpoint path.
            page_param: Name of pagination parameter.
            max_pages: Maximum pages to fetch (None for all).

        Returns:
            pd.DataFrame: Combined paginated data.
        """
        all_dfs = []
        page = 1
        while max_pages is None or page <= max_pages:
            params = {page_param: page}
            df = self.get_dataframe(endpoint, params=params)
            if df.empty:
                break
            all_dfs.append(df)
            page += 1
            # Simple heuristic: if we got fewer than 10 rows, it might be the last page
            if len(df) < 10:
                 break
        
        if not all_dfs:
            return pd.DataFrame()
        return pd.concat(all_dfs, ignore_index=True)


class AuthenticatedAPIClient(APIClient):
    """
    I am an API client with authentication support.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ):
        """
        I initialize the authenticated API client with an API key.

        Args:
            base_url: Base URL for API endpoints.
            api_key: API key for authentication.
            headers: Optional default headers.
            timeout: Request timeout in seconds.
        """
        super().__init__(base_url, headers, timeout)
        self.api_key = api_key
        self.set_auth_header(api_key)

    def refresh_token(self) -> None:
        """
        I refresh the authentication token if it's expired.
        (Placeholder for specific auth implementations)
        """
        pass

    def set_auth_header(self, token: str) -> None:
        """
        I set the authorization header manually.

        Args:
            token: Authentication token.
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
