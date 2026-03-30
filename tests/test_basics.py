
import unittest
import pandas as pd
from src.config import get_config, Config
from src.models import QueryResult, DataSchema

class TestConfig(unittest.TestCase):
    def test_singleton(self):
        c1 = get_config()
        c2 = get_config()
        self.assertIs(c1, c2)

    def test_paths(self):
        config = get_config()
        self.assertTrue(config.project_root.exists())
        self.assertTrue(config.data_dir.exists())
        self.assertTrue(config.dashboard_dir.exists())

class TestModels(unittest.TestCase):
    def test_query_result(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        qr = QueryResult(data=df, query="SELECT *", execution_time=0.1, row_count=2)
        self.assertFalse(qr.is_empty())
        self.assertEqual(qr.row_count, 2)

    def test_data_schema(self):
        df = pd.DataFrame(columns=DataSchema.get_expected_columns("spacex_launches"))
        self.assertTrue(DataSchema.validate_dataframe(df, "spacex_launches"))
        
        df_invalid = pd.DataFrame(columns=["wrong", "columns"])
        self.assertFalse(DataSchema.validate_dataframe(df_invalid, "spacex_launches"))

if __name__ == "__main__":
    unittest.main()
