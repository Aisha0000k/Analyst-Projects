
import unittest
from src import AnalystDashboard, create_app

class TestAnalystDashboard(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_initialization(self):
        self.app.initialize()
        self.assertTrue(self.app._initialized)
        self.assertIsNotNone(self.app.pipeline)
        self.assertIsNotNone(self.app.dashboard)
        self.assertIsNotNone(self.app.cache)

if __name__ == "__main__":
    unittest.main()
