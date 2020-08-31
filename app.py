from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # add
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordlookup.db'  # add
db = SQLAlchemy(app)  # add
migrate = Migrate(app, db)
login_manager = LoginManager(app)

import models

def __repr__(self):
    return '<Grocery %r>' % self.name

@app.shell_context_processor
def make_shell_context():  
    return {'db' : db} 

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
    

if __name__ == '__main__':
    app.run(debug=True)