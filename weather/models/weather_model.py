import requests
import os
import logging
from datetime import datetime, timedelta


class WeatherAPIModel:
    """
    A class to interact with the WeatherAPI and store responses in memory.
    """

    BASE_URL = "http://api.weatherapi.com/v1"
    API_KEY = "f2de263826e5469e9ec205430240612"

    def __init__(self):
        if not self.API_KEY:
            raise ValueError("API key for WeatherAPI.com is not set. Please define WEATHER_API_KEY in the .env file.")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Cache to store API responses in memory
        self.weather_cache = {}

    def _store_in_cache(self, key, data):
        """
        Store weather data in the in-memory cache.

        Args:
            key (str): Unique key for the data (e.g., location+endpoint).
            data (dict): Weather data to store.
        """
        self.weather_cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }

    def _get_from_cache(self, key, max_age_minutes=60):
        """
        Retrieve weather data from the in-memory cache if it is fresh.

        Args:
            key (str): Unique key for the data (e.g., location+endpoint).
            max_age_minutes (int): Maximum age of cached data in minutes.

        Returns:
            dict or None: Cached weather data if available and fresh, None otherwise.
        """
        cached = self.weather_cache.get(key)
        if cached:
            if datetime.now() - cached["timestamp"] <= timedelta(minutes=max_age_minutes):
                self.logger.info(f"Using cached data for key: {key}")
                return cached["data"]
            else:
                self.logger.info(f"Cache expired for key: {key}")
        return None

    def _make_request(self, endpoint, params):
        """
        Helper method to make requests to the WeatherAPI.com API.

        Args:
            endpoint (str): API endpoint to call (e.g., 'current.json').
            params (dict): Query parameters for the request.

        Returns:
            dict: Parsed JSON response from the API.

        Raises:
            RuntimeError: If the API request fails.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        params["key"] = self.API_KEY
        try:
            self.logger.info(f"Making API request to {url} with params {params}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to make API request: {e}")
            raise RuntimeError(f"Failed to fetch data from WeatherAPI: {e}")

    def get_current_weather(self, location):
        """
        Get current weather information for a given location.

        Args:
            location (str): Location name or coordinates.

        Returns:
            dict: Current weather information.
        """
        key = f"{location}-current"
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        data = self._make_request("current.json", {"q": location})
        self._store_in_cache(key, data)
        return data

    def get_forecast(self, location, days=1):
        """
        Get weather forecast for a given location.

        Args:
            location (str): Location name or coordinates.
            days (int): Number of days to fetch the forecast for.

        Returns:
            dict: Weather forecast information.
        """
        key = f"{location}-forecast-{days}"
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        data = self._make_request("forecast.json", {"q": location, "days": days})
        self._store_in_cache(key, data)
        return data

    def get_timezone_info(self, location):
        """
        Get timezone information for a given location.

        Args:
            location (str): Location name or coordinates.

        Returns:
            dict: Timezone information.
        """
        key = f"{location}-timezone"
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        data = self._make_request("timezone.json", {"q": location})
        self._store_in_cache(key, data)
        return data

    def get_astronomy_info(self, location, date):
        """
        Get astronomy information (e.g., sunrise, sunset) for a given location and date.

        Args:
            location (str): Location name or coordinates.
            date (str): Date in YYYY-MM-DD format.

        Returns:
            dict: Astronomy information.
        """
        key = f"{location}-astronomy-{date}"
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        data = self._make_request("astronomy.json", {"q": location, "dt": date})
        self._store_in_cache(key, data)
        return data

    def get_marine_weather(self, location):
        """
        Get marine weather information for a given location.

        Args:
            location (str): Location name or coordinates.

        Returns:
            dict: Marine weather information.
        """
        key = f"{location}-marine"
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        data = self._make_request("marine.json", {"q": location})
        self._store_in_cache(key, data)
        return data

    