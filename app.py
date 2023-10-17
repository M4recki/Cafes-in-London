from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from os import environ
import hashlib

# App


app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("Secret_key_cafe")


# Database


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/cafes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Bootstrap Gravatar, CKEditor


bootstrap = Bootstrap(app)

ckeditor = CKEditor(app)

gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)