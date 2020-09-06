from flask import render_template, flash, redirect, url_for, request
from app import app
from models import User, Superlatives, Words, Brands, Grocery, Uom, Prohibited
from forms import LoginForm
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.urls import url_parse
from forms import RegistrationForm
from app import db
import sys
import re
from sqlalchemy import and_, or_, not_
import sqlalchemy.exc as sqlalchemy_exc

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()  
    if form.validate_on_submit():
        print(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
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

####### USER ADMIN #####
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.admin != 1: 
        return "You are not admin"
    
    else:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            updated_by = current_user.username
            admin = request.form['admin']
            user = User(username=username, email=email, first_name=first_name, last_name = last_name, updated_by=updated_by, admin=admin)
            user.set_password(request.form['password'])
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/admin')
            except:
                return "Problem addmin new user" 
        else:
            users = User.query.order_by(User.username).all()
            return render_template('admin.html', users=users)    


@app.route('/update/users/<int:id>', methods=['POST','GET'])
@login_required
def updateusers(id):
        users = User.query.get_or_404(id)
        if current_user.admin != 1:
            return "You are not admin"
        
        else:    
            if request.method == 'POST':
                users.username = request.form['username']
                users.email = request.form['email']
                users.first_name = request.form['first_name']
                users.last_name = request.form['last_name']
                users.admin = request.form['admin']
                users.updated_by = request.form['updated_by']
                try:
                    db.session.commit()
                    return redirect('/admin')
                except sqlalchemy_exc.SQLAlchemyError:
                    raise
            else:
                title = "Update Users"
                return render_template('updateusers.html', title=title, users=users)


@app.route('/delete/users/<int:id>')
@login_required
def deleteuser(id):
    delete = User.query.get_or_404(id)
    if current_user.admin != 1:
        return "You are not admin"
    else:
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/admin')
        except:
            return "There was an error deleting the users"




########### Main route ###################
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
        
    

######################SUPERLATIVES################################
@app.route('/update/superlatives/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    superlatives = Superlatives.query.get_or_404(id)
    if request.method == 'POST':
        if request.form['word'] == '':
            return "Word cannot be empty"
        else:
            superlatives.word = request.form['word']
            superlatives.example = request.form['example']
            superlatives.ss1 = request.form['ss1']
            superlatives.ss2 = request.form['ss2']
            superlatives.ss3 = request.form['ss3']
            superlatives.comment = request.form['comment']
            superlatives.updated_by = request.form['updated_by']
            

        try:
            db.session.commit()
            return redirect('/superlatives')
        except sqlalchemy_exc.SQLAlchemyError: 
            raise
    else:
        title = "Update Data"
        return render_template('updatesuperlatives.html', title=title, superlatives=superlatives) 

@app.route('/delete/superlatives/<int:id>')
@login_required
def delete(id):
        delete = Superlatives.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/superlatives')
        except:
            return "There was a problem deleting data"



@app.route('/superlatives', methods=['GET', 'POST'])
def superlatives():
    if request.method == 'POST':
        if request.form['word'] == '':
            return "Word cannot be empty"
        else:
            word = request.form['word']
            example = request.form['example']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']
            superlatives = Superlatives(word=word, example=example, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.username)

            try:
                db.session.add(superlatives)
                db.session.commit()
                return redirect('/superlatives')
            except:
                return "There was a problem adding new stuff."

    else:
        superlatives = Superlatives.query.order_by(Superlatives.updated_when).all()
        return render_template('superlatives.html', superlatives=superlatives)




@app.route('/superlatives/search' , methods=['POST'])
def superlativessearch():
    if request.method == 'POST':
        try:                           
            searchword = request.form['search']
            searchword2  = "%{}%".format(searchword)            
            superlatives = Superlatives.query.filter(Superlatives.word.like(searchword2)).all()
            return render_template('superlatives.html', superlatives=superlatives, searchword=searchword)
        except:
            return "There was an error searching"
    else:
        superlatives = Superlatives.query.order_by(Superlatives.updated_when).all()
        return render_template('superlatives.html', superlatives=superlatives)





########Words###########
@app.route('/update/words/<int:id>', methods=['GET', 'POST'])
@login_required
def wordsupdate(id):
    words = Words.query.get_or_404(id)
    if request.method == 'POST':
        if request.form['ptpt'] == '' and request.form['ptbr'] == '':
            return "Words cannot be empty, either fill word in PT-PT or PT-BR"
        else:
            words.ptpt = request.form['ptpt']
            words.ptbr = request.form['ptbr']
            words.abbreviation = request.form['abbreviation']
            words.ss1 = request.form['ss1']
            words.ss2 = request.form['ss2']
            words.ss3 = request.form['ss3']
            words.comment = request.form['comment']
            words.updated_by = request.form['updated_by']
        try:
            db.session.commit()
            return redirect('/words')
        except sqlalchemy_exc.SQLAlchemyError: 
            raise
    else:
        title = "Update Data"
        return render_template('updatewords.html', title=title, words=words) 

@app.route('/delete/words/<int:id>')
@login_required
def wordsdelete(id):
        delete = Words.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/words')
        except:
            return "There was a problem deleting data"



@app.route('/words', methods=['GET', 'POST'])

def words():
    if request.method == 'POST':
        if request.form['ptpt'] == '' and request.form['ptbr'] == '':
            return "Words cannot be empty, either fill word in PT-PT or PT-BR"
        else:
            ptpt = request.form['ptpt']
            ptbr = request.form['ptbr']
            abbreviation = request.form['abbreviation']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']

            words = Words(ptpt=ptpt, ptbr=ptbr, abbreviation=abbreviation, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.username)

            try:
                db.session.add(words)
                db.session.commit()
                return redirect('/words')
            except:
                return "There was a problem adding new words."
    else:
        
        words = Words.query.order_by(Words.updated_when).all()
        return render_template('words.html', words=words)




@app.route('/words/search' , methods=['POST'])
def wordssearch():
    if request.method == 'POST':
        try:
            searchword = request.form['search']
            searchword2  = "%{}%".format(searchword)            
            words = Words.query.filter(or_((Words.ptbr.like(searchword2)),(Words.ptpt.like(searchword2)),(Words.abbreviation.like(searchword2)))).all()
            return render_template('words.html', words=words, searchword=searchword)
        except:
            return "There was an error searching"
    else:
        words = Words.query.order_by(Words.updated_when).all()
        return render_template('words.html', words=words)




        ########Brands###########
@app.route('/update/brands/<int:id>', methods=['GET', 'POST'])
@login_required
def brandsupdate(id):
    brands = Brands.query.get_or_404(id)
    if request.method == 'POST':
        if request.form['brandname'] == '':
            return "brands cannot be empty"
        else:
            brands.brandname = request.form['brandname']
            brands.abbreviation = request.form['abbreviation']
            brands.ss1 = request.form['ss1']
            brands.ss2 = request.form['ss2']
            brands.ss3 = request.form['ss3']
            brands.comment = request.form['comment']
            brands.updated_by = request.form['updated_by']
        try:
            db.session.commit()
            return redirect('/brands')
        except sqlalchemy_exc.SQLAlchemyError: 
            raise
    else:
        title = "Update Data"
        return render_template('updatebrands.html', title=title, brands=brands) 

@app.route('/delete/brands/<int:id>')
@login_required
def brandsdelete(id):
        delete = Brands.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/brands')
        except:
            return "There was a problem deleting data"



@app.route('/brands', methods=['GET', 'POST'])

def brands():
    if request.method == 'POST':
        if request.form['brandname'] == '':
            return "brands cannot be empty"
        else:
            brandname = request.form['brandname']
            abbreviation = request.form['abbreviation']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']

            brands = Brands(brandname=brandname, abbreviation=abbreviation, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.username)

            try:
                db.session.add(brands)
                db.session.commit()
                return redirect('/brands')
            except:
                return "There was a problem adding new brands."
    else:
        
        brands = Brands.query.order_by(Brands.updated_when).all()
        return render_template('brands.html', brands=brands)




@app.route('/brands/search' , methods=['POST'])
def brandssearch():
    if request.method == 'POST':
        try:                           
            searchword = request.form['search']
            searchword2  = "%{}%".format(searchword)            
            brands = Brands.query.filter(or_((Brands.brandname.like(searchword2)),(Brands.abbreviation.like(searchword2)))).all()
            print('FUCLK THIS')
            print(brands)
            print(searchword)
            return render_template('brands.html', brands=brands, searchword=searchword)
        except:
            return "There was an error searching"
    else:
        brands = Brands.query.order_by(Brands.updated_when).all()
        return render_template('brands.html', brands=brands)





        ########UoM###########
@app.route('/update/uom/<int:id>', methods=['GET', 'POST'])
@login_required
def uomupdate(id):
    uom = Uom.query.get_or_404(id)
    if request.method == 'POST':
        if request.form['unit'] == '':
            return "uom cannot be empty"
        else:
            uom.unit = request.form['unit']
            uom.symbol = request.form['symbol']
            uom.description = request.form['description']
            uom.ss1 = request.form['ss1']
            uom.ss2 = request.form['ss2']
            uom.ss3 = request.form['ss3']
            uom.comment = request.form['comment']
            uom.updated_by = request.form['updated_by']
        try:
            db.session.commit()
            return redirect('/uom')
        except sqlalchemy_exc.SQLAlchemyError: 
            raise
    else:
        title = "Update Data"
        return render_template('updateuom.html', title=title, uom=uom) 

@app.route('/delete/uom/<int:id>')
@login_required
def uomdelete(id):
        delete = Uom.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/uom')
        except:
            return "There was a problem deleting data"



@app.route('/uom', methods=['GET', 'POST'])

def uom():
    if request.method == 'POST':
        if request.form['unit'] == '':
            return "uom cannot be empty"
        else:
            unit = request.form['unit']
            symbol = request.form['symbol']
            description = request.form['description']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']
            

            uom = Uom(unit=unit, symbol=symbol, description=description, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.username)

            try:
                db.session.add(uom)
                db.session.commit()
                return redirect('/uom')
            except:
                return "There was a problem adding new uom."
    else:
        
        uom = Uom.query.order_by(Uom.updated_when).all()
        return render_template('uom.html', uom=uom)




@app.route('/uom/search' , methods=['POST'])
def uomsearch():
    if request.method == 'POST':
        try:                           
            searchword = request.form['search']
            searchword2  = "%{}%".format(searchword)            
            uom = Uom.query.filter(or_((Uom.unit.like(searchword2)),(Uom.symbol.like(searchword2)),(Uom.description.like(searchword2)))).all()
            return render_template('uom.html', uom=uom, searchword=searchword)
        except:
            return "There was an error searching"
    else:
        uom = uom.query.order_by(Uom.updated_when).all()
        return render_template('uom.html', uom=uom)


       


######################Prohibited################################
@app.route('/update/prohibited/<int:id>', methods=['GET', 'POST'])
@login_required
def updateprohibited(id):
    prohibited = Prohibited.query.get_or_404(id)
    if request.method == 'POST':
        if request.form['word'] == '':
            return "Prohibited Word cannot be empty"
        else:
            prohibited.word = request.form['word']
            prohibited.example = request.form['example']
            prohibited.ss1 = request.form['ss1']
            prohibited.ss2 = request.form['ss2']
            prohibited.ss3 = request.form['ss3']
            prohibited.comment = request.form['comment']
            prohibited.updated_by = request.form['updated_by']
            

        try:
            db.session.commit()
            return redirect('/prohibited')
        except sqlalchemy_exc.SQLAlchemyError: 
            raise
    else:
        title = "Update Data"
        return render_template('updateprohibited.html', title=title, prohibited=prohibited) 

@app.route('/delete/prohibited/<int:id>')
@login_required
def deleteprohibited(id):
        delete = Prohibited.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/prohibited')
        except:
            return "There was a problem deleting data"



@app.route('/prohibited', methods=['GET', 'POST'])
def prohibited():
    if request.method == 'POST':
        if request.form['word'] == '':
            return "prohibited Word cannot be empty"
        else:
            word = request.form['word']
            example = request.form['example']
            ss1 = request.form['ss1']
            ss2 = request.form['ss2']
            ss3 = request.form['ss3']
            comment = request.form['comment']
            prohibited = Prohibited(word=word, example=example, ss1=ss1, ss2=ss2,ss3=ss3, comment=comment, updated_by=current_user.username)

            try:
                db.session.add(prohibited)
                db.session.commit()
                return redirect('/prohibited')
            except:
                return "There was a problem adding new stuff."

    else:
        prohibited = Prohibited.query.order_by(Prohibited.updated_when).all()
        return render_template('prohibited.html', prohibited=prohibited)




@app.route('/prohibited/search/<int:id>' , methods=['POST'])
def prohibitedssearch(id):
    if request.method == 'POST':
        try:                           
            searchword = request.form['search']
            searchword2  = "%{}%".format(searchword)            
            prohibited = Prohibited.query.filter(Prohibited.word.like(searchword2)).all()
            return render_template('prohibited.html', prohibited=prohibited, searchword=searchword)
        except:
            return "There was an error searching"
    else:
        prohibited = Prohibited.query.order_by(Prohibited.updated_when).all()
        return render_template('prohibited.html', prohibited=prohibited)