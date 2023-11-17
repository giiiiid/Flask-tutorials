from flask import render_template, url_for, flash, request, redirect
from .models import User, Post
from .forms import RegistrationForm, LoginForm
from flaskblog import app, bcrypt, db


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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Your account has been created!', 'success')
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