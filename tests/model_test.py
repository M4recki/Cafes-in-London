from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from conftest import app, db


db = SQLAlchemy()


# Test user table


class User(UserMixin, db.Model):
    """Represents a user in the application.

    This model defines the structure of the user table in the database, including fields for the user's ID, name, email, and password.

    Args:
        UserMixin (mixin): Provides default implementations for the methods required by the Flask-Login user API.
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


# Test cafe table


class Cafe(db.Model):
    """Represents a cafe in the application.

    This model defines the structure of the cafe table in the database, including fields for the cafe's ID, name, description, map URL, image URL, location, availability of sockets, toilet, WiFi, and ability to take calls, as well as the number of seats and the coffee price.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    map_url = db.Column(db.Text)
    img_url = db.Column(db.Text)
    location = db.Column(db.String(50))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String(100))
    coffee_price = db.Column(db.String(100))
    comments = db.relationship("Comment", backref="cafe", lazy=True)


# Test comment table


class Comment(db.Model):
    """Represents a comment on a cafe.

    This model defines the structure of the comment table in the database, including fields for the comment ID, the comment text, and the ID of the cafe the comment is associated with.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"), nullable=False)
