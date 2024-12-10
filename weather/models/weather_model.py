from dataclasses import dataclass
import logging
import sqlite3
import os
from typing import Any
import requests

from weather.utils.sql_utils import get_db_connection
from weather.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class WeatherAPIModel:
    """
    A class for interacting with the WeatherAPI.com API.
    """

    BASE_URL = "http://api.weatherapi.com/v1"
    API_KEY = "f2de263826e5469e9ec205430240612"

    def __init__(self):
        if not self.API_KEY:
            raise ValueError("API key for WeatherAPI.com is not set. Please define WEATHER_API_KEY in the .env file.")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

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

        Raises:
            ValueError: If the location is invalid.
        """
        if not location or not isinstance(location, str):
            self.logger.error("Invalid location provided for current weather.")
            raise ValueError("Location must be a non-empty string.")
        try:
            return self._make_request("current.json", {"q": location})
        except RuntimeError as e:
            self.logger.error(f"Error fetching current weather for location {location}: {e}")
            raise

    def get_forecast(self, location, days=1):
        """
        Get weather forecast for a given location.

        Args:
            location (str): Location name or coordinates.
            days (int): Number of days to fetch the forecast for (default is 1).

        Returns:
            dict: Weather forecast information.

        Raises:
            ValueError: If the location or days parameter is invalid.
        """
        if not location or not isinstance(location, str):
            self.logger.error("Invalid location provided for forecast.")
            raise ValueError("Location must be a non-empty string.")
        if not isinstance(days, int) or days < 1:
            self.logger.error("Invalid days parameter provided for forecast.")
            raise ValueError("Days must be a positive integer.")
        try:
            return self._make_request("forecast.json", {"q": location, "days": days})
        except RuntimeError as e:
            self.logger.error(f"Error fetching forecast for location {location}: {e}")
            raise

    def get_timezone_info(self, location):
        """
        Get timezone information for a given location.

        Args:
            location (str): Location name or coordinates.

        Returns:
            dict: Timezone information.

        Raises:
            ValueError: If the location is invalid.
        """
        if not location or not isinstance(location, str):
            self.logger.error("Invalid location provided for timezone info.")
            raise ValueError("Location must be a non-empty string.")
        try:
            return self._make_request("timezone.json", {"q": location})
        except RuntimeError as e:
            self.logger.error(f"Error fetching timezone info for location {location}: {e}")
            raise

    def get_astronomy_info(self, location, date):
        """
        Get astronomy information (e.g., sunrise, sunset) for a given location and date.

        Args:
            location (str): Location name or coordinates.
            date (str): Date in YYYY-MM-DD format.

        Returns:
            dict: Astronomy information.

        Raises:
            ValueError: If the location or date is invalid.
        """
        if not location or not isinstance(location, str):
            self.logger.error("Invalid location provided for astronomy info.")
            raise ValueError("Location must be a non-empty string.")
        if not date or not isinstance(date, str):
            self.logger.error("Invalid date provided for astronomy info.")
            raise ValueError("Date must be a non-empty string in YYYY-MM-DD format.")
        try:
            return self._make_request("astronomy.json", {"q": location, "dt": date})
        except RuntimeError as e:
            self.logger.error(f"Error fetching astronomy info for location {location} on date {date}: {e}")
            raise

    def get_marine_weather(self, location):
        """
        Get marine weather information (e.g., tide heights) for a given location.

        Args:
            location (str): Location name or coordinates.

        Returns:
            dict: Marine weather information.

        Raises:
            ValueError: If the location is invalid.
        """
        if not location or not isinstance(location, str):
            self.logger.error("Invalid location provided for marine weather.")
            raise ValueError("Location must be a non-empty string.")
        try:
            return self._make_request("marine.json", {"q": location})
        except RuntimeError as e:
            self.logger.error(f"Error fetching marine weather for location {location}: {e}")
            raise