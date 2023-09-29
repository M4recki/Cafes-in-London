from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, RadioField, ValidationError, SubmitField
from wtforms.validators import DataRequired, Email, URL
from app import app, db
from models import User, Cafe, Comment

# Suggest cafe form

class SuggestCafeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()]) 
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField('Has sockets')
    has_toilet = BooleanField('Has toilet')
    has_wifi = BooleanField('Has WiFi')
    can_take_calls = BooleanField('Can take calls')
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    

# Register form

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    checkbox = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        with app.app_context():
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email already exists. Please login or use a different email.')
    
    def validate_password(self, password):
        if password.data != self.confirm_password.data:
            raise ValidationError('Passwords do not match. Please try again.')
        
# Login form

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
# Contact form

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')