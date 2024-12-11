import os
import logging
from flask import Flask, jsonify, request, make_response
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from weather.db import db
from weather.utils.logger import configure_logger
from weather.models.user_model import Users
from weather.models.weather_model import WeatherAPIModel

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
configure_logger(logger)

# Initialize WeatherAPIModel
weather_api = WeatherAPIModel()


def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: Configured Flask app.
    """
    app = Flask(__name__)

    # Load configuration from environment
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./db/user.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Log the database URI for debugging
    logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize database
    db.init_app(app)
    with app.app_context():
        if not os.path.exists('./db/user.db'):
            logger.info("Database file not found. Creating new database.")
            db.create_all()
        else:
            logger.info("Database file exists. Skipping creation.")

    # Routes (as provided, with no changes unless explicitly mentioned)
    ##########################################################
    # Health Check
    ##########################################################
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint to ensure the app is running.

        Returns:
            Response: JSON with health status.
        """
        logger.info("Health check endpoint hit.")
        return jsonify({"status": "healthy"}), 200

    ##########################################################
    # User Management Endpoints
    ##########################################################
    @app.route('/api/create-user', methods=['POST'])
    def create_user():
        """
        Create a new user.
        """
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({"error": "Username and password are required."}), 400)

            Users.create_user(username, password)
            return jsonify({"message": f"User {username} created successfully."}), 201
        except IntegrityError:
            return jsonify({"error": "Username already exists."}), 400
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return jsonify({"error": "Failed to create user."}), 500

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user():
        """
        Delete a user.
        """
        try:
            data = request.get_json()
            username = data.get('username')

            if not username:
                return make_response(jsonify({"error": "Username is required."}), 400)

            Users.delete_user(username)
            return jsonify({"message": f"User {username} deleted successfully."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return jsonify({"error": "Failed to delete user."}), 500

    ##########################################################
    # Weather Endpoints
    ##########################################################
    @app.route('/api/weather/current', methods=['GET'])
    def get_current_weather():
        """
        Get current weather for a location.
        """
        try:
            location = request.args.get('location')
            if not location:
                return make_response(jsonify({"error": "Location is required."}), 400)

            weather_data = weather_api.get_current_weather(location)
            return jsonify(weather_data), 200
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            return jsonify({"error": "Failed to fetch weather data."}), 500
        
    @app.route('/api/weather/forecast', methods=['GET'])
    def get_weather_forecast():
        """
        Get weather forecast for a location.

        Query Parameters:
            - location (str): Location name or coordinates.
            - days (int): Number of forecast days.

        Returns:
            Response: JSON with forecast data or error.
        """
        try:
            location = request.args.get('location')
            days = request.args.get('days', 1, type=int)

            if not location:
                return make_response(jsonify({"error": "Location is required."}), 400)

            forecast_data = weather_api.get_forecast(location, days)
            return jsonify(forecast_data), 200
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return jsonify({"error": "Failed to fetch forecast data."}), 500
        
    @app.route('/api/weather/timezone', methods=['GET'])
    def get_timezone_info():
        """
        Get timezone information for a location.

        Query Parameters:
            - location (str): Location name or coordinates.

        Returns:
            Response: JSON with timezone data or error.
        """
        try:
            # Extract location from query parameters
            location = request.args.get('location')
            if not location:
                return make_response(jsonify({"error": "Location is required."}), 400)

            # Call the WeatherAPIModel to fetch timezone information
            timezone_data = weather_api.get_timezone_info(location)
            
            # Check if "location" exists in the response
            if "location" in timezone_data:
                return jsonify(timezone_data), 200
            else:
                return jsonify({"error": "Failed to retrieve valid timezone data."}), 404

        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            logger.error(f"Error fetching timezone info: {e}")
            return jsonify({"error": "Failed to fetch timezone info."}), 500
        
    @app.route('/api/weather/astronomy', methods=['GET'])
    def get_astronomy_info():
        """
        Get astronomy information for a location on a specific date.

        Query Parameters:
            - location (str): Location name or coordinates.
            - date (str): Date in YYYY-MM-DD format.

        Returns:
            Response: JSON with astronomy data or error.
        """
        try:
            # Extract query parameters
            location = request.args.get('location')
            date = request.args.get('date')

            # Validate parameters
            if not location or not date:
                return make_response(jsonify({"error": "Location and date are required."}), 400)

            # Fetch astronomy information
            astronomy_data = weather_api.get_astronomy_info(location, date)

            # Check if "astronomy" exists in the response
            if "astronomy" in astronomy_data:
                return jsonify(astronomy_data), 200
            else:
                return jsonify({"error": "Failed to retrieve valid astronomy data."}), 404

        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            logger.error(f"Error fetching astronomy info: {e}")
            return jsonify({"error": "Failed to fetch astronomy info."}), 500
        
    @app.route('/api/weather/marine', methods=['GET'])
    def get_marine_weather():
        """
        Get marine weather information for a location.

        Query Parameters:
            - location (str): Location name or coordinates.

        Returns:
            Response: JSON with marine weather data or error.
        """
        try:
            # Extract the 'location' query parameter
            location = request.args.get('location')
            if not location:
                return make_response(jsonify({"error": "Location is required."}), 400)

            # Fetch marine weather data using the WeatherAPIModel instance
            marine_weather_data = weather_api.get_marine_weather(location)

            # Check if 'marine' exists in the response
            if marine_weather_data and isinstance(marine_weather_data, dict):
                return jsonify(marine_weather_data), 200
            else:
                return jsonify({"error": "Failed to retrieve valid marine weather data."}), 404

        except RuntimeError as e:
            # Handle known runtime errors
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            # Log unexpected exceptions and return a generic error message
            logger.error(f"Error fetching marine weather: {e}")
            return jsonify({"error": "Failed to fetch marine weather."}), 500

    ##########################################################
    # Database Management
    ##########################################################
    @app.route('/api/init-db', methods=['POST'])
    def init_db():
        """
        Initialize or recreate the database.
        """
        try:
            db_path = os.getenv("DB_PATH", "/tmp/db/user.db")
            logger.info(f"Initializing database at: {db_path}")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure the directory exists
            with app.app_context():
                db.drop_all()
                db.create_all()
            return jsonify({"message": "Database initialized successfully."}), 200
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            return jsonify({"error": "Failed to initialize database."}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)