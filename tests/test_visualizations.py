
import unittest
import pandas as pd
import os
from src.visualizations.dynamic import PlotlyDashboard

class TestPlotlyDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = PlotlyDashboard(title="Test Dashboard")
        self.df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    def test_add_line_chart(self):
        self.dashboard.add_line_chart(self.df, "x", ["y"], "Line Chart")
        self.assertEqual(len(self.dashboard.figures), 1)

    def test_save_html(self):
        self.dashboard.add_line_chart(self.df, "x", ["y"], "Line Chart")
        path = "tests/test_dashboard.html"
        self.dashboard.save_html(path)
        self.assertTrue(os.path.exists(path))
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    unittest.main()
