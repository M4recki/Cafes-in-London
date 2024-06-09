import pytest
from project.main import app as main_app
from flask import Response


# Pytest fixture to create a app


@pytest.fixture(scope="module")
def app():
    """Provides a Flask app instance for testing.

    This fixture creates a Flask app instance, configures it for testing (using an in-memory SQLite database, disabling SQLAlchemy track modifications, and enabling testing mode), and creates the database tables. After each test, the database is cleaned up by removing all data.

    Yields:
        Flask: The Flask app instance.
    """
    app = main_app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    yield app


# Pytest fixture to create a client


@pytest.fixture(scope="module")
def client(app):
    """Provides a test client for the Flask app.

    This fixture creates a test client for the Flask app, which can be used to make requests to the app during testing.

    Args:
        app (Flask): The Flask app instance.

    Returns:
        FlaskClient: The test client for the Flask app.
    """
    return app.test_client()
