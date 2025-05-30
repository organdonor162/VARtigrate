import os
import dotenv
import requests



def test_noaa_api_key():
    """Test if NOAA API key is set in environment variables."""
    nws_api_key = os.getenv("NOAA_API_KEY")
    if not nws_api_key:
        raise ValueError("NOAA_API_KEY is not set in the environment variables.")
    return nws_api_key

def test_eia_api_key():
    """Test if EIA API key is set in environment variables."""
    eia_api_key = os.getenv("EIA_API_KEY")
    if not eia_api_key:
        raise ValueError("EIA_API_KEY is not set in the environment variables.")
    return eia_api_key

def test_openweather_api_key():
    """Test if OpenWeather API key is set in environment variables."""
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if not openweather_api_key:
        raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")
    return openweather_api_key


def test_eia_api_get():
    try:
        eia_api_key = test_eia_api_key()
        # Use a valid series_id, e.g., 'ELEC.PRICE.US-ALL.M'
        eia_url = f"https://api.eia.gov/v2/?api_key={eia_api_key}&series_id=ELEC.PRICE.US-ALL.M"
        eia_response = requests.get(eia_url)
        eia_response.raise_for_status()
        print("EIA API is working.")
    except requests.exceptions.RequestException as e:
        print(f"Error testing EIA API: {e}")

def test_noaa_api_get():
    try:
        noaa_url = "https://api.weather.gov/gridpoints/LWX/96,70"
        headers = {
            "User-Agent": "VARtigrateApp (gordondoore@gmail.com)",
            "Accept": "application/geo+json"
        }
        noaa_response = requests.get(noaa_url, headers=headers)
        noaa_response.raise_for_status()
        print("NOAA API is working.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error testing NOAA API: {e}")

def test_openweather_api_get():
    #now test api get requests
    try:
        openweather_api_key = test_openweather_api_key()
        openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={openweather_api_key}"
        openweather_response = requests.get(openweather_url)
        openweather_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error testing OpenWeather API: {e}")


if __name__ == "__main__":
    dotenv.load_dotenv()  # Load environment variables from .env file
    test_eia_api_get()
    test_noaa_api_get()
    print("All API tests completed.")

