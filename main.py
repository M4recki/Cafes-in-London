from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from os import environ
from datetime import datetime

@app.route('/')
def home():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run()