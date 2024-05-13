from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5


# Gravatar config


def gravatar(email, size=50, rating="g", default="retro", force_default=False):
    """
    Generates a URL for a Gravatar image based on the provided email address.

    Gravatar is a service that provides globally unique avatars. This function constructs a URL
    to retrieve the avatar image associated with the given email address. The URL includes parameters
    for specifying the size, rating, default image, and whether to force the use of the default image.

    Args:
        email (str): The email address used to identify the Gravatar image. This should be a valid
                     email address registered with Gravatar.
        size (int, optional): The size of the Gravatar image in pixels. Defaults to 50.
        rating (str, optional): The content rating for the Gravatar image. Defaults to "g" (general).
        default (str, optional): The default image to display if the Gravatar image cannot be found.
                                 Defaults to "retro".
        force_default (bool, optional): Whether to force the use of the default image. Defaults to False.

    Returns:
        str: The URL to the Gravatar image.
    """
    hash_value = md5(email.lower().encode("utf-8")).hexdigest()

    url = f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"

    return url


# Login manager


login_manager = LoginManager()


# Database


db = SQLAlchemy()
