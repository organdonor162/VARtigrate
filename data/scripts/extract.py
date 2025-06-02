"""
extract.py
This file defines api calls, largely to gridstatus API, but also open-meteo API, to extract data for the VARtigrate data pipeline.

Date created: 2025-06-02
Last modified: 2025-06-02
Author: Gordon Doore
"""

from typing import List, Dict, Any
from gridstatus import CAISO
import pandas as pd
import requests 

class GridStatusExtractor:
    """
    Class to extract data from the gridstatus API.
    """
    
    def __init__(self, region: str):
        self.caiso = CAISO(region=region)

    def get_historical_load_hourly(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical load data from the gridstatus API.
        
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format.
        :return: DataFrame containing historical load data.
        """
        start = pd.Timestamp("January 1, 2019").normalize()
        end = pd.Timestamp.now().normalize()
        historical_load = self.caiso.get_load(start, end= end)
        # Convert 'Time' to datetime (removes timezone if present)
        historical_load['Time'] = pd.to_datetime(historical_load['Time'], utc = True)

        # Now set index and resample (aggregate only numeric columns)
        historical_hourly_load = historical_load.set_index("Time").resample("h").mean(numeric_only=True)
        return historical_hourly_load
    
    def current_load(self, prev_hours: int = 0):
        """
        Get current load data from the gridstatus API.
        
        :param prev_hours: Number of previous hours to include in the data.
        :return: DataFrame containing current load data.
        """
        current_load = self.caiso.get_load()
        # Convert 'Time' to datetime (removes timezone if present)
        current_load['Time'] = pd.to_datetime(current_load['Time'], utc=True)
        # Set index and resample (aggregate only numeric columns)
        current_load = current_load.set_index("Time").resample("h").mean(numeric_only=True)
        # If prev_hours is specified, filter the DataFrame to include only the last 'prev_hours' hours
        if prev_hours > 0:
            current_load = current_load.last(f"{prev_hours}H")

        return current_load