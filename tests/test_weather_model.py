import pytest
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from weather.models.weather_model import WeatherAPIModel

@pytest.fixture
def weather_api():
    """Fixture to provide a WeatherAPIModel instance."""
    return WeatherAPIModel()

@patch("weather.models.weather_model.requests.get")
def test_get_current_weather_cache(mock_get, weather_api):
    """Test that current weather is fetched from cache if available."""
    location = "Boston"
    cached_data = {"temp": "22°C"}
    weather_api._store_in_cache(f"{location}-current", cached_data)

    result = weather_api.get_current_weather(location)

    assert result == cached_data, "Expected data from cache."
    mock_get.assert_not_called(), "API should not be called if data is in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_current_weather_api_call(mock_get, weather_api):
    """Test that current weather is fetched via API if not in cache."""
    location = "Boston"
    api_response = {"temp": "22°C"}
    mock_get.return_value = MagicMock(status_code=200, json=lambda: api_response)

    result = weather_api.get_current_weather(location)

    assert result == api_response, "Expected data from API."
    mock_get.assert_called_once(), "API should be called if data is not in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_forecast_cache(mock_get, weather_api):
    """Test that forecast is fetched from cache if available."""
    location = "Boston"
    days = 3
    cached_data = {"forecast": "Sunny"}
    weather_api._store_in_cache(f"{location}-forecast-{days}", cached_data)

    result = weather_api.get_forecast(location, days)

    assert result == cached_data, "Expected data from cache."
    mock_get.assert_not_called(), "API should not be called if data is in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_forecast_api_call(mock_get, weather_api):
    """Test that forecast is fetched via API if not in cache."""
    location = "Boston"
    days = 3
    api_response = {"forecast": "Sunny"}
    mock_get.return_value = MagicMock(status_code=200, json=lambda: api_response)

    result = weather_api.get_forecast(location, days)

    assert result == api_response, "Expected data from API."
    mock_get.assert_called_once(), "API should be called if data is not in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_timezone_cache(mock_get, weather_api):
    """Test that timezone info is fetched from cache if available."""
    location = "Boston"
    cached_data = {"timezone": "EST"}
    weather_api._store_in_cache(f"{location}-timezone", cached_data)

    result = weather_api.get_timezone_info(location)

    assert result == cached_data, "Expected data from cache."
    mock_get.assert_not_called(), "API should not be called if data is in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_timezone_api_call(mock_get, weather_api):
    """Test that timezone info is fetched via API if not in cache."""
    location = "Boston"
    api_response = {"timezone": "EST"}
    mock_get.return_value = MagicMock(status_code=200, json=lambda: api_response)

    result = weather_api.get_timezone_info(location)

    assert result == api_response, "Expected data from API."
    mock_get.assert_called_once(), "API should be called if data is not in cache."


@patch("weather.models.weather_model.requests.get")
def test_cache_expiry(mock_get, weather_api):
    """Test that expired cache triggers an API call."""
    location = "Boston"
    cached_data = {"temp": "22°C"}
    weather_api.weather_cache[f"{location}-current"] = {
        "data": cached_data,
        "timestamp": datetime.now() - timedelta(minutes=61)
    }
    api_response = {"temp": "23°C"}
    mock_get.return_value = MagicMock(status_code=200, json=lambda: api_response)

    result = weather_api.get_current_weather(location)

    assert result == api_response, "Expected data from API due to expired cache."
    mock_get.assert_called_once(), "API should be called for expired cache."


@patch("weather.models.weather_model.requests.get")
def test_get_astronomy_info_cache(mock_get, weather_api):
    """Test that astronomy info is fetched from cache if available."""
    location = "Boston"
    date = "2024-12-10"
    cached_data = {"sunrise": "6:00 AM", "sunset": "5:00 PM"}
    weather_api._store_in_cache(f"{location}-astronomy-{date}", cached_data)

    result = weather_api.get_astronomy_info(location, date)

    assert result == cached_data, "Expected data from cache."
    mock_get.assert_not_called(), "API should not be called if data is in cache."


@patch("weather.models.weather_model.requests.get")
def test_get_astronomy_info_api_call(mock_get, weather_api):
    """Test that astronomy info is fetched via API if not in cache."""
    location = "Boston"
    date = "2024-12-10"
    api_response = {"sunrise": "6:00 AM", "sunset": "5:00 PM"}
    mock_get.return_value = MagicMock(status_code=200, json=lambda: api_response)

    result = weather_api.get_astronomy_info(location, date)

    assert result == api_response, "Expected data from API."
    mock_get.assert_called_once(), "API should be called if data is not in cache."