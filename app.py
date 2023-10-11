from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from os import environ
from flask_login import LoginManager
import psycopg2

# App

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("Secret_key_cafe")

# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/cafes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bootstrap Gravatar, CKEditor

bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)