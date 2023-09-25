from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from os import environ
from datetime import datetime

# Home page

@app.route('/')
def home():
    return render_template('main_page.html')

# Register page

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register_page.html')

# Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')

# Contact page

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact_page.html')

# Suggest cafe page

@app.route('/suggest', methods=['GET', 'POST'])
def suggest_cafe():
    return render_template('suggest_cafe_page.html')

# Cafe details page

@app.route('/cafe_details', methods=['GET', 'POST'])
def cafe_details():
    return render_template('cafe_details_page.html')

if __name__ == '__main__':
    app.run(debug=True)