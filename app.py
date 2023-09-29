from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

# App

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database

db = SQLAlchemy(app)