# Weather Application API

## Overview
The Weather Application API provides endpoints to manage user accounts and retrieve weather-related information such as current conditions, forecasts, timezone data, astronomy details, and marine weather. It also includes utilities for health checks and database initialization.

## Routes

### 1. Health Check
- **Path:** `/api/health`
- **Request Type:** `GET`
- **Purpose:** Verifies if the API is up and running.
- **Request Format:** None
- **Response Format:**
  ```json
  {
      "status": "ok"
  }
  ```
- **Example:**
  ```bash
  curl -X GET http://localhost:5000/api/health
  ```

### 2. Create User
- **Path:** `/api/create-user`
- **Request Type:** `POST`
- **Purpose:** Creates a new user account.
- **Request Format:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response Format:**
  ```json
  {
      "message": "User created successfully",
      "user_id": "integer"
  }
  ```
- **Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "secure_pass"}' \
  http://localhost:5000/api/create-user
  ```

### 3. Delete User
- **Path:** `/api/delete-user`
- **Request Type:** `DELETE`
- **Purpose:** Deletes an existing user account.
- **Request Format:**
  ```json
  {
      "user_id": "integer"
  }
  ```
- **Response Format:**
  ```json
  {
      "message": "User deleted successfully"
  }
  ```
- **Example:**
  ```bash
  curl -X DELETE -H "Content-Type: application/json" \
  -d '{"user_id": 123}' \
  http://localhost:5000/api/delete-user
  ```

### 4. Current Weather
- **Path:** `/api/weather/current`
- **Request Type:** `GET`
- **Purpose:** Fetches the current weather for a specified location.
- **Request Format:**
  `GET` parameters:
  - `location`: String, required

- **Response Format:**
  ```json
  {
      "location": "string",
      "temperature": "float",
      "condition": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/api/weather/current?location=New%20York"
  ```

### 5. Weather Forecast
- **Path:** `/api/weather/forecast`
- **Request Type:** `GET`
- **Purpose:** Fetches weather forecasts for a specified location.
- **Request Format:**
  `GET` parameters:
  - `location`: String, required
  - `days`: Integer, optional (default: 3)

- **Response Format:**
  ```json
  {
      "location": "string",
      "forecasts": [
          {
              "date": "string",
              "temperature": "float",
              "condition": "string"
          }
      ]
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/api/weather/forecast?location=New%20York&days=5"
  ```

### 6. Timezone Data
- **Path:** `/api/weather/timezone`
- **Request Type:** `GET`
- **Purpose:** Retrieves timezone data for a specified location.
- **Request Format:**
  `GET` parameters:
  - `location`: String, required

- **Response Format:**
  ```json
  {
      "location": "string",
      "timezone": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/api/weather/timezone?location=New%20York"
  ```

### 7. Astronomy Data
- **Path:** `/api/weather/astronomy`
- **Request Type:** `GET`
- **Purpose:** Fetches astronomy-related data for a specified location.
- **Request Format:**
  `GET` parameters:
  - `location`: String, required

- **Response Format:**
  ```json
  {
      "location": "string",
      "sunrise": "string",
      "sunset": "string"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/api/weather/astronomy?location=New%20York"
  ```

### 8. Marine Weather
- **Path:** `/api/weather/marine`
- **Request Type:** `GET`
- **Purpose:** Fetches marine weather information for a specified location.
- **Request Format:**
  `GET` parameters:
  - `location`: String, required

- **Response Format:**
  ```json
  {
      "location": "string",
      "wave_height": "float",
      "sea_temperature": "float"
  }
  ```
- **Example:**
  ```bash
  curl -X GET "http://localhost:5000/api/weather/marine?location=New%20York"
  ```

### 9. Initialize Database
- **Path:** `/api/init-db`
- **Request Type:** `POST`
- **Purpose:** Initializes the database with default configurations.
- **Request Format:** None
- **Response Format:**
  ```json
  {
      "message": "Database initialized successfully"
  }
  ```
- **Example:**
  ```bash
  curl -X POST http://localhost:5000/api/init-db
  ```

