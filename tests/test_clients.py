
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.data.api.base_client import APIClient
from src.data.database.supabase import SupabaseClient
from src.config import get_config

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(base_url="https://api.test.com")

    @patch('requests.Session.request')
    def test_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        result = self.client.get("endpoint")
        self.assertEqual(result, {"key": "value"})
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_get_dataframe(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        df = self.client.get_dataframe("endpoint")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["id", "name"])

class TestSupabaseClient(unittest.TestCase):
    def setUp(self):
        self.config = get_config()
        self.client = SupabaseClient(self.config)

    def test_initial_state(self):
        self.assertFalse(self.client._connected)
        self.assertIsNone(self.client.client)

if __name__ == "__main__":
    unittest.main()
