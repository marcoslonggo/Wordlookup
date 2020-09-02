from flask import render_template, flash, redirect, url_for, request
from app import app
from models import User, Superlatives, Grocery
from forms import LoginForm
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.urls import url_parse
from forms import RegistrationForm
from app import db
import sys
import re
import sqlalchemy.exc as sqlalchemy_exc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for_('index'))
    form  = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/update/superlatives/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    superlatives = Superlatives.query.get_or_404(id)
    if request.method == 'POST':
            
            
            superlatives.word = request.form['word']
            example = request.form['example']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']
            updated_by = request.form['updated_by']
            

            try:
               #db.session.add(superlatives)
               db.session.commit()
               return redirect('/superlatives')
            except sqlalchemy_exc.SQLAlchemyError: 
                raise
    else:
        title = "Update Data"
        return render_template('updatesuperlatives.html', title=title, superlatives=superlatives) 

@app.route('/delete/superlatives/<int:id>')
#@login_required
def delete(id):
        delete = Superlatives.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/superlatives')
        except:
            return "There was a problem deleting data"



@app.route('/superlatives', methods=['GET', 'POST'])
@login_required
def superlatives():
    if request.method == 'POST':
        word = request.form['word']
        example = request.form['example']
        ss1 = request.form['ss1']
        ss2 = request.form['ss2']
        ss3 = request.form['ss3']
        comment = request.form['comment']
        superlatives = Superlatives(word=word, example=example, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.id)

        try:
            db.session.add(superlatives)
            db.session.commit()
            return redirect('/superlatives')
        except:
            return "There was a problem adding new stuff."

    else:
        superlatives = Superlatives.query.order_by(Superlatives.updated_when).all()
        return render_template('superlatives.html', superlatives=superlatives)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocery(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        return render_template('index.html', groceries=groceries)

#@login_required
#def index():
#    return render_template("index.html", title='Home Page')

