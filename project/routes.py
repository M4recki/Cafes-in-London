from project.extensions import db
from project.models import User, Cafe, SuggestCafe, Comment
from project.forms import (
    RegisterForm,
    LoginForm,
    ContactForm,
    CafeForm,
    CommentForm,
    PreviewCafeForm,
)
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    request,
    abort,
    Blueprint,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy import func
from os import environ
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
from functools import wraps


main = Blueprint("main", __name__)


# Admin decorator


def admin_required(f):
    """Decorator to restrict access to admin-only routes.

    This decorator checks if the current user is an admin (user.id == 1) before allowing access to the decorated route. If the user is not an admin, the function will return a 403 Forbidden response.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# Current year in footer


@main.context_processor
def current_year():
    """Adds the current year to the template context.

    This function is used as a context processor to make the current year available in all templates.

    Returns:
        dict: A dictionary containing the current year.
    """
    current_year = datetime.now().year
    return {"current_year": current_year}


# Home page


@main.route("/")
def home():
    """Renders the home page template with a list of cafes.

    This function queries the Cafe model to get all the cafes and passes them to the 'main_page.html' template.

    Returns:
        str: The rendered HTML template.
    """
    cafes = Cafe.query.all()
    return render_template("main_page.html", cafes=cafes)


# Cafe details page


@main.route("/cafe/<int:cafe_id>", methods=["GET", "POST"])
def cafe_details(cafe_id):
    from project.extensions import gravatar

    """Renders the cafe details page and handles commenting on the cafe.
    
        This function retrieves the cafe and its comments from the database, and renders the 'cafe_details_page.html' template with the cafe and comment form. If the comment form is submitted, a new comment is added to the database.
    
        Args:
            cafe_id (int): The ID of the cafe to display.
    
        Returns:
            str: The rendered HTML template.
        """
    cafe = Cafe.query.get(cafe_id)
    comments = Comment.query.filter_by(cafe_id=cafe_id).all()
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash("You must be logged in to comment.")
            return redirect(url_for("main.login"))
        comment = Comment(
            comment=form.comment.data, cafe_id=cafe_id, comment_author=current_user.id
        )

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("main.cafe_details", cafe_id=cafe_id))

    return render_template(
        "cafe_details_page.html",
        cafe=cafe,
        form=form,
        user=current_user,
        gravatar=gravatar,
    )


# Delete comment


@main.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    """Deletes a comment from the database.

    This function retrieves the comment with the given ID, deletes it from the database, and redirects the user back to the cafe details page.

    Args:
        comment_id (int): The ID of the comment to delete.

    Returns:
        str: A redirect to the cafe details page.
    """
    comment = Comment.query.get(comment_id)
    cafe_id = comment.cafe_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.cafe_details", cafe_id=cafe_id))


# Edit comment


@main.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    """Allows a user to edit a comment.

    This function retrieves the comment with the given ID, and renders the 'cafe_details_page.html' template with a pre-populated comment form. If the form is submitted, the comment is updated in the database and the user is redirected to the cafe details page.

    Args:
        comment_id (int): The ID of the comment to edit.

    Returns:
        str: The rendered HTML template or a redirect to the cafe details page.
    """
    comment = Comment.query.get(comment_id)
    cafe_id = comment.cafe_id
    cafe = Cafe.query.get(cafe_id)
    form = CommentForm(comment=comment.comment)
    db.session.delete(comment)
    db.session.commit()

    if form.validate_on_submit():

        comment.comment = form.comment.data
        db.session.commit()

        return redirect(url_for("main.cafe_details", cafe_id=cafe_id))

    return render_template("cafe_details_page.html", form=form, cafe=cafe)


# Delete cafe from main page


@main.route("/delete_cafe/<int:cafe_id>")
@login_required
@admin_required
def delete_cafe_home(cafe_id):
    """Deletes a cafe from the database.

    This function retrieves the cafe with the given ID, deletes it from the database, and redirects the user back to the home page.

    Args:
        cafe_id (int): The ID of the cafe to delete.

    Returns:
        str: A redirect to the home page.
    """
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("main.home"))


# Edit cafe from main page


@main.route("/edit_cafe/<int:cafe_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_cafe(cafe_id):
    """Allows an admin to edit the details of a cafe.

    This function retrieves the cafe with the given ID, and renders the 'edit_cafe_page.html' template with a pre-populated cafe form. If the form is submitted, the cafe details are updated in the database and the user is redirected to the home page.

    Args:
        cafe_id (int): The ID of the cafe to edit.

    Returns:
        str: The rendered HTML template or a redirect to the home page.
    """
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm(description=cafe.description)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data

        cafe.name = name
        cafe.description = description
        cafe.map_url = map_url
        cafe.img_url = img_url
        cafe.location = location
        cafe.has_sockets = has_sockets
        cafe.has_toilet = has_toilet
        cafe.has_wifi = has_wifi
        cafe.can_take_calls = can_take_calls
        cafe.seats = seats
        cafe.coffee_price = coffee_price

        db.session.commit()

        return redirect(url_for("main.home"))

    flash_messages = get_flashed_messages()
    return render_template(
        "edit_cafe_page.html", form=form, cafe=cafe, flash_messages=flash_messages
    )


# Register page


@main.route("/register", methods=["GET", "POST"])
def register():
    """Handles user registration.

    This function renders the 'register_page.html' template with a registration form. If the form is submitted and validated, a new user is created in the database, the user is logged in, and the user is redirected to the home page. If the email already exists, a flash message is displayed and the user is redirected back to the registration page.

    Returns:
        str: The rendered HTML template or a redirect to the home page.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please login or use a different email.")
            return redirect(url_for("main.register"))

        else:
            hash_and_salted_password = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8
            )
            new_user = User(email=email, password=hash_and_salted_password, name=name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("main.home"))

    flash_messages = get_flashed_messages()
    return render_template(
        "register_page.html", form=form, flash_messages=flash_messages
    )


# Login page


@main.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login.

    This function renders the 'login_page.html' template with a login form. If the form is submitted and validated, the user is logged in and redirected to the home page. If the email does not exist or the password is incorrect, a flash message is displayed and the user is redirected back to the login page.

    Returns:
        str: The rendered HTML template or a redirect to the home page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("main.login"))

        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("main.login"))

        else:
            login_user(user)
            return redirect(url_for("main.home"))

    flash_messages = get_flashed_messages()
    return render_template("login_page.html", form=form, flash_messages=flash_messages)


# Logout page


@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Logs out the current user and redirects them to the home page.

    This function logs out the current user using the `logout_user()` function, and then redirects the user to the home page.

    Returns:
        str: A redirect to the home page.
    """
    logout_user()
    return redirect(url_for("main.home"))


# Send email function


def send_email(email_address, subject, message):
    """Sends an email using the Gmail SMTP server.

    This function creates an EmailMessage object with the provided email address, subject, and message, and then sends the email using the Gmail SMTP server. The email receiver address and password are fetched from environment variables.

    Args:
        email_address (str): The email address to send the message from.
        subject (str): The subject of the email.
        message (str): The content of the email message.
    """
    email_receiver = environ.get("EMAIL_RECEIVER_TODO")
    password = environ.get("EMAIL_PASSWORD_CAFE")

    email = EmailMessage()

    email["From"] = email_address
    email["To"] = email_receiver
    email["Subject"] = subject
    email.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_receiver, password)
        smtp.sendmail(email_address, email_receiver, email.as_string())


# Contact page


@main.route("/contact", methods=["GET", "POST"])
def contact():
    """Handles the contact form submission.

    This function renders the 'contact_page.html' template with a contact form. If the form is submitted and validated, the `send_email()` function is called to send an email to the configured email receiver, and the user is redirected to the home page.

    Returns:
        str: The rendered HTML template or a redirect to the home page.
    """
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = f"{name}, {email} - {form.subject.data}"
        message = form.message.data

        send_email(email, subject, message)

        return redirect(url_for("main.home"))

    flash_messages = get_flashed_messages()
    return render_template(
        "contact_page.html", form=form, flash_messages=flash_messages
    )


# Suggest cafe page


@main.route("/suggest", methods=["GET", "POST"])
@login_required
def suggest_cafe():
    """Handles the cafe suggestion form submission.

    This function renders the 'suggest_cafe_page.html' template with a cafe suggestion form. If the form is submitted and validated, a new `SuggestCafe` record is created in the database with the provided information, and the user is redirected to the home page.

    Returns:
        str: The rendered HTML template or a redirect to the home page.
    """
    form = CafeForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data

        cafe_suggestion = SuggestCafe(
            name=name,
            description=description,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price,
            suggestion_author=current_user.id,
        )

        db.session.add(cafe_suggestion)
        db.session.commit()

        return redirect(url_for("main.home"))

    flash_messages = get_flashed_messages()
    return render_template(
        "suggest_cafe_page.html", form=form, flash_messages=flash_messages
    )


# Select cafe suggestion to add page


@main.route("/add_cafe", methods=["GET", "POST"])
@login_required
@admin_required
def choose_cafe():
    """Allows an admin to select a cafe suggestion to add to the main page.

    This function retrieves all the cafe suggestions from the database, and renders the 'choose_cafe_page.html' template with a dropdown form to select a cafe. If the form is submitted, the user is redirected to the preview cafe page.

    Returns:
        str: The rendered HTML template.
    """
    cafes = SuggestCafe.query.all()
    form = PreviewCafeForm()
    form.cafe_pick.choices = [(cafe.id, cafe.name) for cafe in cafes]

    if form.validate_on_submit():
        if "submit" in request.form:
            return redirect(url_for("main.preview_cafe", cafe_id=form.cafe_pick.data))

    return render_template("choose_cafe_page.html", form=form)


# Preview cafe suggestion page


@main.route("/preview_cafe/<int:cafe_id>", methods=["GET", "POST"])
@login_required
@admin_required
def preview_cafe(cafe_id):
    """Allows an admin to preview a selected cafe suggestion.

    This function retrieves the cafe suggestion with the given ID and renders the 'preview_cafe_page.html' template with the cafe details.

    Args:
        cafe_id (int): The ID of the cafe suggestion to preview.

    Returns:
        str: The rendered HTML template.
    """
    cafe = SuggestCafe.query.get(cafe_id)
    return render_template("preview_cafe_page.html", cafe=cafe)


# Delete cafe suggestion


@main.route("/delete_cafe/<int:cafe_id>")
@login_required
@admin_required
def delete_cafe_suggestion(cafe_id):
    """Deletes a suggested cafe from the database.

    This function retrieves the suggested cafe with the given ID, deletes it from the database, and redirects the user back to the home page.

    Args:
        cafe_id (int): The ID of the suggested cafe to delete.

    Returns:
        str: A redirect to the home page.
    """
    cafe = SuggestCafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("main.home"))


# Add cafe suggestion to home page


@main.route("/add_cafe/<int:cafe_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_cafe_suggestion(cafe_id):
    """Adds a suggested cafe to the main cafe list.

    This function retrieves the suggested cafe with the given ID, creates a new Cafe object with the suggested cafe's details, adds the new cafe to the database, and deletes the suggested cafe. The user is then redirected to the home page.

    Args:
        cafe_id (int): The ID of the suggested cafe to add.

    Returns:
        str: A redirect to the home page.
    """
    suggest_cafe = SuggestCafe.query.get(cafe_id)
    max_id = db.session.query(func.max(Cafe.id)).scalar()

    new_cafe = Cafe(
        id=max_id + 1,
        name=suggest_cafe.name,
        description=suggest_cafe.description,
        map_url=suggest_cafe.map_url,
        img_url=suggest_cafe.img_url,
        location=suggest_cafe.location,
        has_sockets=suggest_cafe.has_sockets,
        has_toilet=suggest_cafe.has_toilet,
        has_wifi=suggest_cafe.has_wifi,
        can_take_calls=suggest_cafe.can_take_calls,
        seats=suggest_cafe.seats,
        coffee_price=suggest_cafe.coffee_price,
    )

    db.session.add(new_cafe)
    db.session.delete(suggest_cafe)
    db.session.commit()

    return redirect(url_for("main.home"))
