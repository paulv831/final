import pytest
from flask import Flask
from weather.db import db

@pytest.fixture
def app():
    """
    Create and configure a new app instance for testing.
    """
    app = Flask(__name__)

    # Set configuration for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables
        yield app
        db.session.remove()
        db.drop_all()  # Drop tables after test

@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    return app.test_client()