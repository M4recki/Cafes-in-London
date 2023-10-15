from flask_login import UserMixin
from app import app, db

# User table


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


# Cafe table


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)
    comments = db.relationship("Comment", backref=db.backref("cafe", lazy=True))


# Suggest cafe table


class SuggestCafe(db.Model):
    __tablename__ = "suggest_cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=True)
    map_url = db.Column(db.Text, nullable=False, unique=True)
    img_url = db.Column(db.Text, nullable=False, unique=True)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False, default=False)
    has_toilet = db.Column(db.Boolean, nullable=False, default=False)
    has_wifi = db.Column(db.Boolean, nullable=False, default=False)
    can_take_calls = db.Column(db.Boolean, nullable=False, default=False)
    seats = db.Column(db.String(10), nullable=False)
    coffee_price = db.Column(db.String(10), nullable=False)
    suggestion_author = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    suggestion_author_name = db.relationship("User", backref=db.backref("suggest_cafe", lazy=True))
    


# Comment table


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"), nullable=False)
    comment_author = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_author_name = db.relationship("User", backref=db.backref("comments", lazy=True))
    
    
with app.app_context():
    db.create_all()
    db.session.commit()