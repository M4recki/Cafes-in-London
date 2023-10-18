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
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


# Contact form


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


# Comment form


class CommentForm(FlaskForm):
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Preview cafe form
class PreviewCafeForm(FlaskForm):
    cafe_pick = SelectField("Choose a cafe", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Preview")
