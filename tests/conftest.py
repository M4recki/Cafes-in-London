import pytest
from project.main import app as main_app
from project.models import User, Cafe, Comment, db
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
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


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


# Pytest fixture to clean up the database after each test


@pytest.fixture(autouse=True)
def clean_database(client, app):
    """Cleans up the database after each test.

    This fixture deletes all data from the User, Cafe, and Comment tables in the database after each test is run.

    Args:
        client (FlaskClient): The test client for the Flask app.
        app (Flask): The Flask app instance.
    """

    with app.app_context():
        db.session.query(User).delete()
        db.session.query(Cafe).delete()
        db.session.query(Comment).delete()
        db.session.commit()
