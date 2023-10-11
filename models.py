from flask_login import UserMixin
from app import app, db
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash
from flask_gravatar import Gravatar


# User table


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    
    def gravatar(self):
        gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


# Cafe table


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)


# Suggest cafe table


class SuggestCafe(db.Model):
    __tablename__ = "suggest_cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)


# Comment table


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_name = db.Column(db.String(100), db.ForeignKey("users.name"))
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"))
    user = db.relationship("User", backref=db.backref("comments", lazy=True))
    cafe = db.relationship("Cafe", backref=db.backref("comments", lazy=True))
    
with app.app_context():
    db.create_all()
