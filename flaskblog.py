from flask import Flask, render_template, url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import *

# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '964565dbc835b0ed7dbefe7248cffbcf'
# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __str__(self):
        return f'{self.username}, {self.email}'
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'Post({self.title}, {self.date})'

# views/logic
@app.route('/')
def home():
    return render_template('home.html', title='FlaskBlog')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    # if request.method == 'POST':
    #     name = request.form['username']
    #     email = request.form['email']
    #     password = request.form['password']
    #     confirm_password = request.form['confirm_password']

    #     if password == confirm_password:
    #         flash(f'Account created for {form.username.data}!', 'success')
    #         return redirect(url_for('login'))
    #     else:
    #         flash(f'Passwords do not match!', 'error')
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match')
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'aa':
            flash(f'{form.username.data} has  logged in')
            return redirect(url_for('home'))
        else:
            flash(f'Invalid credentials')
        
    return render_template('login.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)
