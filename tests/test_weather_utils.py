import pytest
from weather.utils.weather_utils import (
    validate_location,
    validate_date,
    format_weather_response,
    convert_temperature,
    format_datetime,
    extract_sunrise_sunset
)


def test_validate_location():
    """Test the validation of location input."""
    # Valid input
    assert validate_location("Boston") == "Boston"
    assert validate_location("   New York  ") == "New York"

    # Invalid input
    with pytest.raises(ValueError, match="Location must be a non-empty string."):
        validate_location("")
    with pytest.raises(ValueError, match="Location must be a non-empty string."):
        validate_location(None)
    with pytest.raises(ValueError, match="Location must be a non-empty string."):
        validate_location(123)


def test_validate_date():
    """Test the validation and parsing of date strings."""
    # Valid input
    assert validate_date("2024-12-10") == pytest.approx(
        datetime.date(2024, 12, 10)
    )

    # Invalid input
    with pytest.raises(ValueError, match="Date must be in the format 'YYYY-MM-DD'."):
        validate_date("10-12-2024")
    with pytest.raises(ValueError, match="Date must be in the format 'YYYY-MM-DD'."):
        validate_date("2024/12/10")
    with pytest.raises(ValueError, match="Date must be in the format 'YYYY-MM-DD'."):
        validate_date("InvalidDate")


def test_format_weather_response():
    """Test the formatting of weather API responses."""
    response = {
        "temp_c": 22.5,
        "humidity": 60,
        "condition": "Sunny"
    }

    # Valid keys
    formatted = format_weather_response(response, ["temp_c", "humidity"])
    assert formatted == {"temp_c": 22.5, "humidity": 60}

    # Missing keys
    formatted = format_weather_response(response, ["wind_speed"])
    assert formatted == {}

    # Invalid response
    with pytest.raises(ValueError, match="Response must be a dictionary."):
        format_weather_response("InvalidResponse", ["temp_c"])
    with pytest.raises(ValueError, match="Keys must be a list of strings."):
        format_weather_response(response, "temp_c")


def test_convert_temperature():
    """Test the conversion of temperatures."""
    # Valid conversions
    assert convert_temperature(32, "C") == 0  # Fahrenheit to Celsius
    assert convert_temperature(0, "F") == 32  # Celsius to Fahrenheit

    # Invalid unit
    with pytest.raises(ValueError, match="Unit must be 'C' for Celsius or 'F' for Fahrenheit."):
        convert_temperature(32, "K")


def test_format_datetime():
    """Test the formatting of ISO 8601 datetime strings."""
    # Valid input
    assert format_datetime("2024-12-10T15:30:00") == "2024-12-10 15:30:00"

    # Invalid input
    with pytest.raises(ValueError, match="Datetime string must be in ISO 8601 format."):
        format_datetime("10-12-2024 15:30")
    with pytest.raises(ValueError, match="Datetime string must be in ISO 8601 format."):
        format_datetime("InvalidDateTime")


def test_extract_sunrise_sunset():
    """Test the extraction of sunrise and sunset times."""
    response = {
        "astronomy": {
            "astro": {
                "sunrise": "6:00 AM",
                "sunset": "5:00 PM"
            }
        }
    }

    # Valid response
    result = extract_sunrise_sunset(response)
    assert result == {"sunrise": "6:00 AM", "sunset": "5:00 PM"}

    # Missing keys
    response = {"astronomy": {}}
    result = extract_sunrise_sunset(response)
    assert result == {"sunrise": "Unknown", "sunset": "Unknown"}

    # Invalid response
    with pytest.raises(ValueError, match="Response must be a dictionary."):
        extract_sunrise_sunset("InvalidResponse")