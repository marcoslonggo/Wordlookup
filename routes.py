from flask import render_template, flash, redirect, url_for, request
from app import app
from models import User
from forms import LoginForm
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.urls import url_parse
from forms import RegistrationForm
from app import db


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





@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery.query.get_or_404(id)
    if request.method == 'POST':
            grocery.name = request.form['name']
            try:
               db.session.commit()
               return redirect('/')
            except:
                return "There was a problem updating data."
    else:
        title = "Update Data"
        return render_template('update.html', title=title, grocery=grocery) 

@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data"

@app.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    return render_template("index.html", title='Home Page')

