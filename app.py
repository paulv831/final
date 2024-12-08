import bcrypt
import requests
from flask import Flask, jsonify, request, make_response
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask and SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Environment Variable (Replace with your WeatherAPI key)
WEATHER_API_KEY = "f2de263826e5469e9ec205430240612"

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check route to verify the service is running."""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/create-account', methods=['POST'])
def create_account():
    """Create a new user account with a username, password, and location."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    location = data.get('location')

    if not username or not password or not location:
        raise BadRequest("Username, password, and location are required.")

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    # Save user to the database
    new_user = User(username=username, hashed_password=hashed_password.decode(), salt=salt.decode(), location=location)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"Account created for {username}"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login route to verify the username and password."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise BadRequest("Username and password are required.")

    user = User.query.filter_by(username=username).first()
    if not user:
        raise Unauthorized("Invalid username or password.")

    # Verify password
    if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
        raise Unauthorized("Invalid username or password.")

    return jsonify({"message": f"Welcome back, {username}!"}), 200

@app.route('/api/update-password', methods=['POST'])
def update_password():
    """Update the password for a user."""
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        raise BadRequest("Username, old password, and new password are required.")

    user = User.query.filter_by(username=username).first()
    if not user:
        raise Unauthorized("Invalid username or password.")

    # Verify old password
    if not bcrypt.checkpw(old_password.encode(), user.hashed_password.encode()):
        raise Unauthorized("Invalid old password.")

    # Hash the new password and update it
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode(), salt)

    user.hashed_password = hashed_password.decode()
    user.salt = salt.decode()
    db.session.commit()

    return jsonify({"message": f"Password updated for {username}"}), 200

# WeatherAPI Helper
def fetch_weather_api(endpoint, params):
    base_url = f"http://api.weatherapi.com/v1/{endpoint}.json"
    params['key'] = WEATHER_API_KEY
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

@app.route('/api/weather/current', methods=['GET'])
def current_weather():
    """Get current weather for the user's location."""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        raise BadRequest("User not found.")

    weather = fetch_weather_api("current", {"q": user.location})
    return jsonify({
        "location": weather['location']['name'],
        "temperature": weather['current']['temp_c'],
        "condition": weather['current']['condition']['text']
    }), 200

@app.route('/api/weather/timezone', methods=['GET'])
def timezone():
    """Get timezone information for the user's location."""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        raise BadRequest("User not found.")

    weather = fetch_weather_api("current", {"q": user.location})
    return jsonify({
        "timezone": weather['location']['tz_id'],
        "local_time": weather['location']['localtime']
    }), 200

@app.route('/api/weather/forecast', methods=['GET'])
def weather_forecast():
    """Get weather forecast for the user's location."""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        raise BadRequest("User not found.")

    forecast = fetch_weather_api("forecast", {"q": user.location, "days": 3})
    return jsonify({
        "forecast": forecast['forecast']['forecastday']
    }), 200

@app.route('/api/weather/astro', methods=['GET'])
def astro():
    """Get astro information (sunrise/sunset) for the user's location."""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        raise BadRequest("User not found.")

    forecast = fetch_weather_api("forecast", {"q": user.location, "days": 1})
    astro_data = forecast['forecast']['forecastday'][0]['astro']
    return jsonify({
        "sunrise": astro_data['sunrise'],
        "sunset": astro_data['sunset']
    }), 200

@app.route('/api/weather/marine', methods=['GET'])
def marine_weather():
    """Get marine weather information for the user's location."""
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if not user:
        raise BadRequest("User not found.")

    marine = fetch_weather_api("marine", {"q": user.location})
    return jsonify({
        "marine_weather": marine.get('data', "No marine data available.")
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
