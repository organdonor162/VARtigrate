import unittest
from unittest.mock import patch, Mock
from eia_collector import EIADataCollector  # adjust import if needed
import pandas as pd

class TestEIADataCollector(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.collector = EIADataCollector(api_key=self.api_key)

    @patch("eia_collector.requests.Session.get")
    def test_get_electricity_demand(self, mock_get):
        mock_data = {
            "response": {
                "data": [
                    {
                        "period": "2024-01-01T00",
                        "respondent": "US48",
                        "value": 12345
                    }
                ]
            }
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        df = self.collector.get_electricity_demand()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertIn("timestamp", df.columns)
        self.assertEqual(df.iloc[0]["demand_mw"], 12345)

    @patch("eia_collector.requests.Session.get")
    def test_get_renewable_generation(self, mock_get):
        mock_data = {
            "response": {
                "data": [
                    {
                        "period": "2024-01-01T00",
                        "respondent": "US48",
                        "fueltype": "SUN",
                        "value": 6789
                    }
                ]
            }
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        df = self.collector.get_renewable_generation()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.iloc[0]["generation_mw"], 6789)
        self.assertEqual(df.iloc[0]["fuel_type"], "SUN")

    @patch("eia_collector.requests.Session.get")
    def test_get_electric_hourly_demand_subregion(self, mock_get):
        mock_data = {
            "response": {
                "data": [
                    {
                        "period": "2024-01-01T01",
                        "respondent": "US48",
                        "value": 1111
                    }
                ]
            }
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        df = self.collector.get_electric_hourly_demand_subregion()

        self.assertEqual(df.iloc[0]["demand_mw"], 1111)
        self.assertEqual(df.iloc[0]["region"], "US48")

    @patch("eia_collector.requests.Session.get")
    def test_make_request_error_handling(self, mock_get):
        mock_get.side_effect = Exception("API down")

        with self.assertRaises(Exception):
            self.collector._make_request("invalid-endpoint")

if __name__ == "__main__":
    unittest.main()
