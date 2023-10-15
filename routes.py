from app import app, db, gravatar
from models import User, Cafe, SuggestCafe, Comment
from forms import RegisterForm, LoginForm, ContactForm, SuggestCafeForm, CommentForm, PreviewCafeForm
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from os import environ
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
from functools import wraps


# Login manager

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin decorator

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Current year in footer

@app.context_processor
def current_year():
    current_year = datetime.now().year
    return {'current_year': current_year}


# Home page

@app.route('/')
def home():
    cafes = Cafe.query.all()
    return render_template('main_page.html', cafes=cafes)

# Cafe details page

@app.route('/cafe/<int:cafe_id>', methods=['GET', 'POST'])
def cafe_details(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash('You must be logged in to comment.')
            return redirect(url_for('login'))
        comment = Comment(comment=form.comment.data, cafe_id=cafe_id, comment_author=current_user.id)
        
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('cafe_details', cafe_id=cafe_id))


    return render_template('cafe_details_page.html', cafe=cafe, form=form, user=current_user, gravatar=gravatar)   
    
# Edit comment

@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)
    form = CommentForm(text=comment.text)
    if form.validate_on_submit():
        comment.text = form.text.data
        db.session.commit()
        return redirect(url_for('cafe', cafe_id=comment.cafe_id))
    return render_template('edit_comment.html', form=form, comment=comment)

# Delete comment

@app.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('cafe', cafe_id=comment.cafe_id))

# Edit cafe from main page

@app.route('/edit_cafe/<int:cafe_id>', methods=['GET', 'POST'])
@login_required
@admin_required
@admin_required
def edit_cafe_home(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    

# Delete cafe from main page

@app.route('/delete_cafe/<int:cafe_id>')
@login_required
@admin_required
def delete_cafe_home(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))

# Register page

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please login or use a different email.')
            return redirect(url_for('register'))
        
        else:
            hash_and_salted_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=email,
                password=hash_and_salted_password,
                name=name
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        
    flash_messages = get_flashed_messages()
    return render_template('register_page.html', form=form, flash_messages=flash_messages)

# Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('That email does not exist, please try again.')
            return redirect(url_for('login'))
        
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        
        else:
            login_user(user)
            return redirect(url_for('home'))
        
    flash_messages = get_flashed_messages()
    return render_template('login_page.html', form=form, flash_messages=flash_messages)

# Logout page

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Send email function

def send_email(email_address, subject, message):
    email_receiver = environ.get('EMAIL_RECEIVER_TODO')
    password = environ.get('EMAIL_PASSWORD_TODO')
    
    email = EmailMessage()
    
    email['From'] = email_address
    email['To'] = email_receiver
    email['Subject'] = subject
    email.set_content(message)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_address, password)
        smtp.sendmail(email_address, email_receiver, email.as_string())

# Contact page

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        
        send_email(email, subject, message)
        
        return redirect(url_for('home'))
    
    flash_messages = get_flashed_messages()
    return render_template('contact_page.html', form=form, flash_messages=flash_messages)

# Suggest cafe page

@app.route('/suggest', methods=['GET', 'POST'])
@login_required
def suggest_cafe():
    form = SuggestCafeForm()
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
        
        cafe_suggestion = SuggestCafe(name=name, description=description, map_url=map_url, img_url=img_url, location=location, has_sockets=has_sockets, has_toilet=has_toilet, has_wifi=has_wifi, can_take_calls=can_take_calls, seats=seats, coffee_price=coffee_price, suggestion_author=current_user.id)
        
        db.session.add(cafe_suggestion)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    flash_messages = get_flashed_messages()
    return render_template('suggest_cafe_page.html', form=form, flash_messages=flash_messages)

# Select cafe suggestion to add page

@app.route('/add_cafe', methods=['GET', 'POST'])
@login_required
@admin_required
def choose_cafe():
    cafes = SuggestCafe.query.all()
    form = PreviewCafeForm()
    form.cafe_pick.choices = [(cafe.id, cafe.name) for cafe in cafes]
    
    if form.validate_on_submit():
        if 'submit' in request.form:
            return redirect(url_for('preview_cafe', cafe_id=form.cafe_pick.data))    
    
    return render_template('choose_cafe_page.html', form=form)


# Preview cafe suggestion page

@app.route('/preview_cafe/<int:cafe_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def preview_cafe(cafe_id):
    cafe = SuggestCafe.query.get(cafe_id)
    return render_template('preview_cafe_page.html', cafe=cafe)


# Delete cafe suggestion

@app.route('/delete_cafe/<int:cafe_id>')
@login_required
@admin_required
def delete_cafe_suggestion(cafe_id):
    cafe = SuggestCafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('home'))


# Add cafe suggestion to home page

@app.route('/move_cafe/<int:cafe_id>', methods=['POST'])
@login_required
@admin_required
def add_cafe_suggestion(cafe_id):
    suggest_cafe = SuggestCafe.query.get(cafe_id)

    new_cafe = Cafe(
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
        coffee_price=suggest_cafe.coffee_price
    )
    
    db.session.add(new_cafe)
    db.session.delete(suggest_cafe)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)