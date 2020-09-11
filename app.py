from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Yabadabadoo'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordlookup.db'  
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ptwordlookup:Pwb9NMabTGX6sHk@ptwordlookup.longo.com.br/ptwordlookup'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kmzhrgjwynsquf:8ebd2b217894767fa7b778c43f3ceb539af561e85ef5c53aa6144d8ae0070cf5@ec2-52-21-247-176.compute-1.amazonaws.com:5432/d3gh9b2i23ld11'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

import routes
import models

def __repr__(self):
    return '<Grocery %r>' % self.name


if __name__ == '__main__':
    app.run(debug=True)