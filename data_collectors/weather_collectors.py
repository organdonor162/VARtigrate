import requests
import pandas as pd
import time
from datetime import datetime
from typing import Dict, List, Tuple
import logging
import os
from dotenv import load_dotenv

load_dotenv()
mail = os.getenv("EMAIL")
logger = logging.getLogger(__name__)

class OpenWeatherCollector:
    """Collector for OpenWeatherMap data"""
    
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

class NOAACollector:
    """Collector for NOAA/NWS data"""
    def __init__(self):
        self.base_url = "https://api.weather.gov"
        self.session = requests.Session()
        # Set User-Agent as required by NWS API
        self.session.headers.update({
            'User-Agent': f'VARtigrate/1.0 ({mail})'
        })
    
    def get_gridpoint(self, lat: float, lon: float) -> Tuple[str, int, int]:
        """Get NWS gridpoint for coordinates"""
        try:
            response = self.session.get(f"{self.base_url}/points/{lat},{lon}")
            response.raise_for_status()
            data = response.json()
            
            properties = data['properties']
            office = properties['gridId']
            grid_x = properties['gridX']
            grid_y = properties['gridY']
            
            return office, grid_x, grid_y
            
        except requests.exceptions.RequestException as e:
            logger.error(f"NOAA gridpoint request failed: {e}")
            raise
    
    def get_forecast(self, lat: float, lon: float) -> pd.DataFrame:
        """Get 7-day forecast from NOAA"""
        try:
            office, grid_x, grid_y = self.get_gridpoint(lat, lon)
            time.sleep(0.5)  # Rate limiting
            
            # Get hourly forecast
            response = self.session.get(
                f"{self.base_url}/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"
            )
            response.raise_for_status()
            data = response.json()
            
            records = []
            for period in data['properties']['periods']:
                records.append({
                    'timestamp': pd.to_datetime(period['startTime']),
                    'latitude': lat,
                    'longitude': lon,
                    'temperature_c': (period['temperature'] - 32) * 5/9 if period['temperatureUnit'] == 'F' else period['temperature'],
                    'wind_speed_ms': self._parse_wind_speed(period.get('windSpeed', '0 mph')),
                    'wind_direction': period.get('windDirection', 'N'),
                    'forecast_text': period.get('shortForecast', ''),
                    'data_source': 'NOAA'
                })
            
            return pd.DataFrame(records)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"NOAA forecast request failed: {e}")
            raise
    
    def _parse_wind_speed(self, wind_speed_str: str) -> float:
        """Parse wind speed string like '10 mph' to m/s"""
        try:
            speed_mph = float(wind_speed_str.split()[0])
            return speed_mph * 0.44704  # Convert mph to m/s
        except (ValueError, IndexError):
            return 0.0



def main():
    # Set your coordinates (example: New York City)
    lat = 40.7128
    lon = -74.0060

    # # Test OpenWeatherCollector
    # openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    # if not openweather_api_key:
    #     raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")

    # print("=== OpenWeather Current Weather ===")
    # owc = OpenWeatherCollector(openweather_api_key)
    # current_weather = owc.get_current_weather(lat, lon)
    # print(current_weather)

    # print("\n=== OpenWeather 5-Day Forecast ===")
    # forecast_df = owc.get_forecast(lat, lon)
    # print(forecast_df.head())

    # Test NOAACollector
    print("\n=== NOAA 7-Day Hourly Forecast ===")
    noaa = NOAACollector()
    noaa_forecast_df = noaa.get_forecast(lat, lon)
    print(noaa_forecast_df.head())

if __name__ == "__main__":
    main()