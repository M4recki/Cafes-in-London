from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SelectField,
    ValidationError,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, URL

# Suggest cafe form


class CafeForm(FlaskForm):
    """
    Form for suggesting a new cafe to the application.

    This form collects various details about the cafe, including its name, description, map URL,
    image URL, location, amenities, seating capacity, coffee price, and a submit button.
    """

    name = StringField("Cafe Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    map_url = StringField("Cafe Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("District", validators=[DataRequired()])
    has_sockets = BooleanField("Sockets available")
    has_toilet = BooleanField("Toilet available")
    has_wifi = BooleanField("WiFi available")
    can_take_calls = BooleanField("Take calls available")
    seats = StringField("Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Register form


class RegisterForm(FlaskForm):
    """
    Form for user registration.

    This form collects the user's name, email, password, confirmation of the password, agreement
    to terms and conditions, and a submit button. It includes validation to ensure passwords match
    and that all fields are filled out correctly.
    """

    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    checkbox = BooleanField(
        "I agree to the Terms and Conditions", validators=[DataRequired()]
    )
    submit = SubmitField("Register")

    def validate_password(self, password):
        if password.data != self.confirm_password.data:
            raise ValidationError("Passwords do not match. Please try again.")


# Login form


class LoginForm(FlaskForm):
    """
    Form for user login.

    This form collects the user's email and password, and a submit button. It ensures that both
    the email and password fields are filled out correctly.
    """

    email = StringField("Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


# Contact form


class ContactForm(FlaskForm):
    """
    Form for sending a contact message.

    This form collects the user's name, email, subject, message, and a submit button. It ensures
    that all fields are filled out correctly.
    """

    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


# Comment form


class CommentForm(FlaskForm):
    """
    Form for posting a comment.

    This form collects the user's comment and a submit button. It ensures that the comment field
    is filled out correctly.
    """

    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Preview cafe form
class PreviewCafeForm(FlaskForm):
    """
    Form for previewing a selected cafe.

    This form allows the user to choose a cafe from a dropdown menu and submit the selection.
    """

    cafe_pick = SelectField("Choose a cafe", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Preview")
