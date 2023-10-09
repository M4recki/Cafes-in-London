from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, RadioField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Email, URL
from app import app, db
from models import User, Cafe, Comment
from wtforms import TextAreaField

# Suggest cafe form

class SuggestCafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    map_url = StringField('Cafe Map URL', validators=[DataRequired(), URL()]) 
    img_url = StringField('Cafe Image URL', validators=[DataRequired(), URL()])
    district = StringField('District', validators=[DataRequired()])
    sockets_available = BooleanField('Sockets available', validators=[DataRequired()])
    toilet_available = BooleanField('Toilet available', validators=[DataRequired()])
    wifi_available = BooleanField('WiFi available', validators=[DataRequired()])
    take_calls_available = BooleanField('Take calls available', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

# Register form

class RegisterForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    checkbox = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_password(self, password):
        if password.data != self.confirm_password.data:
            raise ValidationError('Passwords do not match. Please try again.')
        
# Login form

class LoginForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    password = PasswordField('Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
# Contact form

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
    
# Comment form

class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')