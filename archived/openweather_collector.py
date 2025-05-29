import requests
import pandas as pd
import logging
from typing import Dict
import os
from dotenv import load_dotenv
load_dotenv()
mail = os.getenv("EMAIL")
logger = logging.getLogger(__name__)


class OpenWeatherCollector:
    """Collector for OpenWeatherMap data
    
    NOT DONE YET, DONT WANT TO PAY YET FOR API KEY
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
    
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather data"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = self.session.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenWeather API request failed: {e}")
            raise
    
    def get_forecast(self, lat: float, lon: float) -> pd.DataFrame:
        """Get 5-day hourly forecast"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = self.session.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()
            
            records = []
            for item in data.get('list', []):
                records.append({
                    'timestamp': pd.to_datetime(item['dt'], unit='s'),
                    'latitude': lat,
                    'longitude': lon,
                    'temperature_c': item['main']['temp'],
                    'humidity_pct': item['main']['humidity'],
                    'wind_speed_ms': item['wind']['speed'],
                    'wind_direction_deg': item['wind'].get('deg', 0),
                    'cloud_cover_pct': item['clouds']['all'],
                    'weather_main': item['weather'][0]['main'],
                    'data_source': 'OpenWeatherMap'
                })
            
            return pd.DataFrame(records)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenWeather forecast request failed: {e}")
            raise