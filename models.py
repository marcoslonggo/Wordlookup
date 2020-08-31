from app import db
from datetime import datetime  # add
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    added_by = db.Column(db.Integer, nullable=False)
    added_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Superlatives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), nullable=False)
    example = db.Column(db.String(120))
    ss1 = db.Column(db.String(120) )
    ss2 = db.Column(db.String(120))
    ss3 = db.Column(db.String(120))
    comment = db.Column(db.String(120))
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    added_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)  