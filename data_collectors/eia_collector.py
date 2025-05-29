#eia collector
#class to collect data from the EIA API

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()

eia_api_key = os.getenv("EIA_API_KEY")
if not eia_api_key:
    raise ValueError("EIA_API_KEY is not set in the environment variables.")

logger = logging.getLogger(__name__)

class EIADataCollector:
    """Class to collect data from the EIA API."""

    def __init__(self, api_key:str):
        self.api_key = api_key
        self.base_url = "https://api.eia.gov/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })


    def _make_request(self, endpoint: str, body: Optional[Dict] = None) -> Dict:
        """Make a POST request to the EIA API."""
        if body is None:
            body = {}

        url = f"{self.base_url}/{endpoint}?api_key={self.api_key}"

        try:
            response = self.session.post(url, json=body)
            response.raise_for_status()
            print(json.dumps(response.json(), indent=2))  # For debugging
            time.sleep(0.1)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"EIA API request failed: {e}")
            raise



    def get_electricity_demand(self, region: str = "US48", 
                                start_date: str = None, 
                                end_date: str = None) -> pd.DataFrame:
        """Get hourly electricity demand data"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%dT%H")

        body = {
            "frequency": "hourly",
            "data": ["value"],
            "facets": {
                "respondent": ["US48"],
                "type": ["D"]  # D = Demand
            },
            "start": start_date,
            "end": end_date,
            "sort": [{"column": "period", "direction": "asc"}],
            "offset": 0,
            "length": 5000,
        }


        data = self._make_request('electricity/rto/region-data', body)

        records = []
        for item in data.get('response', {}).get('data', []):
            records.append({
                'timestamp': pd.to_datetime(item['period']),
                'region': item['respondent'],
                'demand_mw': item['value'],
                'data_source': 'EIA'
            })

        return pd.DataFrame(records)

    def get_renewable_generation(self, region: str = "CISO",
                                 fuel_type: str = "SUN") -> pd.DataFrame:
        """Get renewable generation data (SUN=solar, WND=wind)"""
        body = {
            "frequency": "hourly",
            "data": ["value"],
            "facets": {
                "respondent": [region],
                "fueltype": [fuel_type]
            },
            "sort": [
                {"column": "period", "direction": "desc"}
            ],
            "offset": 0,
            "length": 5000
        }

        data = self._make_request('electricity/rto/fuel-type-data', body)

        records = []
        for item in data.get('response', {}).get('data', []):
            records.append({
                'timestamp': pd.to_datetime(item['period']),
                'region': item['respondent'],
                'fuel_type': item['fueltype'],
                'generation_mw': item['value'],
                'data_source': 'EIA'
            })

        return pd.DataFrame(records)

    def get_electric_hourly_demand_subregion(self, region: str = "US48",
                                             start_date: str = None,
                                             end_date: str = None) -> pd.DataFrame:
        """Get hourly electricity demand data for subregions"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%dT%H")

        body = {
            "frequency": "hourly",
            "data": ["value"],
            "facets": {
                "respondent": [region]
            },
            "start": start_date,
            "end": end_date,
            "sort": [
                {"column": "period", "direction": "desc"}
            ],
            "offset": 0,
            "length": 5000
        }

        data = self._make_request('electricity/rto/subregion-data', body)

        records = []
        for item in data.get('response', {}).get('data', []):
            records.append({
                'timestamp': pd.to_datetime(item['period']),
                'region': item['respondent'],
                'demand_mw': item['value'],
                'data_source': 'EIA'
            })

        return pd.DataFrame(records)


if __name__ == "__main__":
    # Initialize collector
    load_dotenv()
    print(f"API Key from env: {os.getenv('EIA_API_KEY')}")

    eia_api_key = os.getenv("EIA_API_KEY")
    if not eia_api_key:
        raise ValueError("EIA_API_KEY is not set in the environment variables.")
    
    collector = EIADataCollector(api_key = eia_api_key)
    collector = EIADataCollector(eia_api_key)
    print(f"Collector has API key: {collector.api_key}")

    # Example: Get electricity demand for the last 3 days
    # start = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%dT%H")
    # end = datetime.now().strftime("%Y-%m-%dT%H")
    # print("\n=== Electricity Demand Example ===")
    # demand_df = collector.get_electricity_demand(start_date=start, end_date=end)
    # print(demand_df.head())

    # Example: Get solar generation for US48
    print("\n=== Renewable (Solar) Generation Example ===")
    solar_df = collector.get_renewable_generation(fuel_type="SUN")
    print(solar_df.head())

    # Example: Get subregion demand
    print("\n=== Subregion Demand Example ===")
    subregion_df = collector.get_electric_hourly_demand_subregion()
    print(subregion_df.head())
