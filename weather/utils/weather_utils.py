import datetime
import logging

# Initialize logger for the utilities
logger = logging.getLogger(__name__)

def validate_location(location):
    """
    Validates the location input to ensure it is a valid string.

    Args:
        location (str): The location to validate.

    Raises:
        ValueError: If the location is invalid.
    """
    if not isinstance(location, str) or not location.strip():
        logger.error("Invalid location provided: %s", location)
        raise ValueError("Location must be a non-empty string.")
    return location.strip()

def validate_date(date_str):
    """
    Validates and parses a date string in the format 'YYYY-MM-DD'.

    Args:
        date_str (str): The date string to validate.

    Returns:
        datetime.date: A valid date object.

    Raises:
        ValueError: If the date string is invalid or cannot be parsed.
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error("Invalid date format: %s. Expected 'YYYY-MM-DD'.", date_str)
        raise ValueError("Date must be in the format 'YYYY-MM-DD'.")

def format_weather_response(response, keys):
    """
    Extracts and formats specific keys from a weather API response.

    Args:
        response (dict): The weather API response.
        keys (list): A list of keys to extract from the response.

    Returns:
        dict: A dictionary containing the extracted key-value pairs.
    """
    if not isinstance(response, dict):
        logger.error("Invalid API response: %s", response)
        raise ValueError("Response must be a dictionary.")
    if not keys or not isinstance(keys, list):
        logger.error("Invalid keys parameter: %s", keys)
        raise ValueError("Keys must be a list of strings.")

    formatted_response = {key: response.get(key) for key in keys if key in response}
    logger.info("Formatted response: %s", formatted_response)
    return formatted_response

def convert_temperature(temp, unit="C"):
    """
    Converts temperature between Celsius and Fahrenheit.

    Args:
        temp (float): The temperature value to convert.
        unit (str): The target unit ('C' for Celsius, 'F' for Fahrenheit).

    Returns:
        float: The converted temperature value.

    Raises:
        ValueError: If the unit is invalid.
    """
    if unit.upper() == "C":
        return round((temp - 32) * 5 / 9, 2)  # Fahrenheit to Celsius
    elif unit.upper() == "F":
        return round((temp * 9 / 5) + 32, 2)  # Celsius to Fahrenheit
    else:
        logger.error("Invalid temperature unit: %s", unit)
        raise ValueError("Unit must be 'C' for Celsius or 'F' for Fahrenheit.")

def format_datetime(datetime_str):
    """
    Converts an ISO 8601 datetime string to a human-readable format.

    Args:
        datetime_str (str): The ISO 8601 datetime string.

    Returns:
        str: A formatted datetime string.

    Raises:
        ValueError: If the datetime string is invalid.
    """
    try:
        dt = datetime.datetime.fromisoformat(datetime_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error("Invalid datetime string: %s", datetime_str)
        raise ValueError("Datetime string must be in ISO 8601 format.")

def extract_sunrise_sunset(response):
    """
    Extracts sunrise and sunset times from an astronomy API response.

    Args:
        response (dict): The astronomy API response.

    Returns:
        dict: A dictionary with 'sunrise' and 'sunset' times.

    Raises:
        ValueError: If the response is invalid or missing keys.
    """
    if not isinstance(response, dict):
        logger.error("Invalid API response: %s", response)
        raise ValueError("Response must be a dictionary.")

    try:
        astro_data = response.get("astronomy", {}).get("astro", {})
        return {
            "sunrise": astro_data.get("sunrise", "Unknown"),
            "sunset": astro_data.get("sunset", "Unknown")
        }
    except Exception as e:
        logger.error("Failed to extract sunrise/sunset data: %s", str(e))
        raise ValueError("Invalid response format for sunrise/sunset extraction.")