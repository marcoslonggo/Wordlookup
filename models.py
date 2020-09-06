from app import db
from datetime import datetime  # add
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

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
    added_by = db.Column(db.Integer, nullable=True)
    admin = db.Column(db.Integer, nullable=True)
    added_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(128), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Superlatives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), nullable=False, unique=True)
    example = db.Column(db.String(120), nullable=True)
    ss1 = db.Column(db.String(120), nullable=True)
    ss2 = db.Column(db.String(120), nullable=True)
    ss3 = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(120), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ptpt = db.Column(db.String(120), nullable=False, unique=True)
    ptbr = db.Column(db.String(120), nullable=False, unique=True)
    abbreviation = db.Column(db.String(120), nullable=True)
    ss1 = db.Column(db.String(120), nullable=True)
    ss2 = db.Column(db.String(120), nullable=True)
    ss3 = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(120), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brandname = db.Column(db.String(120), nullable=False, unique=True)
    abbreviation = db.Column(db.String(120), nullable=True)
    ss1 = db.Column(db.String(120), nullable=True)
    ss2 = db.Column(db.String(120), nullable=True)
    ss3 = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(120), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Uom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(120), nullable=False, unique=True)
    symbol = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(120), nullable=True)
    ss1 = db.Column(db.String(120), nullable=True)
    ss2 = db.Column(db.String(120), nullable=True)
    ss3 = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(120), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Prohibited(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), nullable=False, unique=True)
    example = db.Column(db.String(120), nullable=True)
    ss1 = db.Column(db.String(120), nullable=True)
    ss2 = db.Column(db.String(120), nullable=True)
    ss3 = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.String(120), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))