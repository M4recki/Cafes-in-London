from flask_login import UserMixin
from project.extensions import db

# User table


class User(UserMixin, db.Model):
    """
    Represents a user in the application.

    Inherits from UserMixin for basic user functionality and db.Model for SQLAlchemy ORM capabilities.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


# Cafe table


class Cafe(db.Model):
    """
    Represents a cafe in the application.

    Stores information about each cafe, such as its name, description, map URL, image URL,
    location, amenities, seating capacity, coffee price, and comments.
    """

    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)
    comments = db.relationship("Comment", backref=db.backref("cafe", lazy=True))


# Suggest cafe table


class SuggestCafe(db.Model):
    """
    Represents a suggested cafe by a user.

    Allows users to suggest new cafes to the application, including details like the cafe's
    name, description, map URL, image URL, location, amenities, seating capacity, coffee price,
    and the author of the suggestion.
    """

    __tablename__ = "suggest_cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    map_url = db.Column(db.Text, nullable=False, unique=True)
    img_url = db.Column(db.Text, nullable=False, unique=True)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False, default=False)
    has_toilet = db.Column(db.Boolean, nullable=False, default=False)
    has_wifi = db.Column(db.Boolean, nullable=False, default=False)
    can_take_calls = db.Column(db.Boolean, nullable=False, default=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)
    suggestion_author = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    suggestion_author_name = db.relationship(
        "User", backref=db.backref("suggest_cafe", lazy=True)
    )


# Comment table


class Comment(db.Model):
    """
    Represents a comment made by a user on a cafe.

    Stores the comment text, the cafe it refers to, and the author of the comment.
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"), nullable=False)
    comment_author = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_author_name = db.relationship(
        "User", backref=db.backref("comments", lazy=True)
    )
