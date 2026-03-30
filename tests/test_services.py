
import unittest
from unittest.mock import MagicMock
import pandas as pd
import shutil
import os
from src.services import DataPipelineService, DashboardService, CacheService

class TestDataPipelineService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.api = MagicMock()
        self.service = DataPipelineService(self.db, self.api)

    def test_transform_data(self):
        df = pd.DataFrame({"A": [1, None], "B": [3, 4]})
        rules = {"fillna": 0, "rename_columns": {"A": "new_A"}}
        result = self.service.transform_data(df, rules)
        self.assertEqual(result["new_A"].iloc[1], 0)
        self.assertIn("new_A", result.columns)

class TestDashboardService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.service = DashboardService(self.db)

    def test_calculate_kpis(self):
        df = pd.DataFrame({"Outcome": [1, 0, 1, 1], "PayloadMass": [1000, 2000, 3000, 4000]})
        kpis = self.service.calculate_kpis(df)
        self.assertEqual(kpis["success_rate"], "75.0%")
        self.assertEqual(kpis["total_launches"], 4)

class TestCacheService(unittest.TestCase):
    def setUp(self):
        self.cache_dir = "tests/test_cache"
        self.service = CacheService(self.cache_dir)

    def tearDown(self):
        self.service.clear_all()
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def test_cache_set_get(self):
        df = pd.DataFrame({"A": [1, 2]})
        self.service.set("key", df)
        result = self.service.get("key")
        pd.testing.assert_frame_equal(df, result)

if __name__ == "__main__":
    unittest.main()
