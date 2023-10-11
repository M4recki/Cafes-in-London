from app import app, db, bootstrap, gravatar, ckeditor
from models import User, Cafe, SuggestCafe, Comment
from forms import RegisterForm, LoginForm, ContactForm, SuggestCafeForm, CommentForm
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from os import environ
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
from functools import wraps
from flask import abort

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

@app.route('/cafe/<int:cafe_id>')
def cafe(cafe_id):
    form = CommentForm()
    cafe = Cafe.query.get(cafe_id)
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to login or register to comment.')
            return redirect(url_for('login'))
        text = form.comment_text.data
        new_comment = Comment(text=text, author_id=current_user.id, cafe_id=cafe_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('cafe', cafe_id=cafe_id))
    else:
        return render_template('cafe_details_page.html', current_user=current_user, cafe=cafe, form=form, gravatar=gravatar)   
    
# Edit comment

@app.route('/edit-comment/<int:comment_id>', methods=['GET', 'POST'])
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

@app.route('/delete-comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('cafe', cafe_id=comment.cafe_id))

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
        cafe_name = form.cafe_name.data
        description = form.description.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        district = form.district.data
        sockets_available = form.sockets_available.data
        toilet_available = form.toilet_available.data
        wifi_available = form.wifi_available.data
        take_calls_available = form.take_calls_available.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        
        cafe_suggestion = SuggestCafe(cafe_name=cafe_name, map_url=map_url, img_url=img_url, district=district, sockets_available=sockets_available, toilet_available=toilet_available, wifi_available=wifi_available, take_calls_available=take_calls_available, seats=seats, coffee_price=coffee_price)
        
        db.session.add(cafe_suggestion)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    flash_messages = get_flashed_messages()
    return render_template('suggest_cafe_page.html', form=form, flash_messages=flash_messages)

# Add new cafe page

@app.route('/add_cafe', methods=['GET', 'POST'])
@login_required
@admin_required
def add_cafe():
    form = SuggestCafeForm()
    cafes = SuggestCafe.query.all()
    return render_template('add_cafe_page.html', form=form, cafes=cafes)

# Preview cafe page

@app.route('/preview_cafe/<int:cafe_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def preview_cafe(cafe_id):
    cafe = SuggestCafe.query.get(cafe_id)
    return render_template('preview_cafe_page.html', cafe=cafe)

# Cafe details page

@app.route('/cafe_details/<int:cafe_id>', methods=['GET', 'POST'])
def cafe_details(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    all_comments = Comment.query.filter_by(cafe_id=cafe_id).all()
    comment_form = CommentForm()
    
    if comment_form.validate_on_submit():
        comment = Comment(user=current_user, cafe_id=cafe_id, comment=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('cafe_details', cafe_id=cafe_id))

    return render_template('cafe_details_page.html', cafe=cafe, all_comments=all_comments, comment_form=comment_form, gravatar=gravatar)

if __name__ == '__main__':
    app.run(debug=True)