from project.extensions import db, login_manager, gravatar
from project.models import User
from project.routes import main
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from os import environ


# App


def create_app(database_uri=environ.get("Cafes_in_London_DB")):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = environ.get("Secret_key_cafe")

    # Database URI

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Login manager

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Bootstrap, ckeditor and gravatar init

    bootstrap = Bootstrap(app)

    ckeditor = CKEditor(app)

    gravatar.init_app(app)

    app.register_blueprint(main)

    return app
