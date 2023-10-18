from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar


# Gravatar config


gravatar = Gravatar(
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)


# Login manager


login_manager = LoginManager()


# Database


db = SQLAlchemy()
