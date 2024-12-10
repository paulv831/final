#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

##############################################
#
# Weather API Tests
#
##############################################

# Function to get current weather
get_current_weather() {
  echo "Fetching current weather for New York..."
  response=$(curl -s -X GET "$BASE_URL/weather/current?location=New+York")
  if echo "$response" | grep -q '"current"'; then
    echo "Current weather fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Current Weather JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch current weather."
    exit 1
  fi
}

# Function to get weather forecast
get_weather_forecast() {
  echo "Fetching 3-day weather forecast for New York..."
  response=$(curl -s -X GET "$BASE_URL/weather/forecast?location=New+York&days=3")
  if echo "$response" | grep -q '"forecast"'; then
    echo "Weather forecast fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Forecast JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch weather forecast."
    exit 1
  fi
}

# Function to get timezone info
get_timezone_info() {
  echo "Fetching timezone info for New York..."
  response=$(curl -s -X GET "$BASE_URL/weather/timezone?location=New+York")
  if echo "$response" | grep -q '"location"'; then
    echo "Timezone info fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Timezone JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch timezone info."
    exit 1
  fi
}

# Function to get astronomy info
get_astronomy_info() {
  echo "Fetching astronomy info for New York on 2024-12-10..."
  response=$(curl -s -X GET "$BASE_URL/weather/astronomy?location=New+York&date=2024-12-10")
  if echo "$response" | grep -q '"astronomy"'; then
    echo "Astronomy info fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Astronomy JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch astronomy info."
    exit 1
  fi
}

# Function to get marine weather
get_marine_weather() {
  echo "Fetching marine weather for Miami..."
  response=$(curl -s -X GET "$BASE_URL/weather/marine?location=Miami")
  if echo "$response" | grep -q '"marine"'; then
    echo "Marine weather fetched successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Marine Weather JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to fetch marine weather."
    exit 1
  fi
}

##############################################
#
# Database Initialization
#
##############################################

# Function to initialize the database
init_db() {
  echo "Initializing the database..."
  response=$(curl -s -X POST "$BASE_URL/init-db")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Database initialized successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Database Initialization JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to initialize the database."
    exit 1
  fi
}

# Run all the steps in order
check_health
init_db
get_current_weather
get_weather_forecast
get_timezone_info
get_astronomy_info
get_marine_weather

echo "All weather API tests passed successfully!"
