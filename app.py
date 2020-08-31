from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Yabadabadoo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordlookup.db'  
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
#login_manager = LoginManager(app)
login = LoginManager(app)
login.login_view = 'login'

import routes
import models

def __repr__(self):
    return '<Grocery %r>' % self.name


if __name__ == '__main__':
    app.run(debug=True)