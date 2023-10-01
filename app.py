from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from os import environ
from flask_login import LoginManager
from flask_gravatar import Gravatar

# App

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("Secret_key_cafe")

# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bootstrap Gravatar, CKEditor

bootstrap = Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)
ckeditor = CKEditor(app)