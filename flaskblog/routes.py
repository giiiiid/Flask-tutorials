from flask import render_template, url_for, flash, request, redirect, request
from .models import User, Post
from .forms import RegistrationForm, LoginForm
from flaskblog import app, bcrypt, db, login_user
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@login_required
def home():
    return render_template('home.html', title='FlaskBlog')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            uname = form.username.data
            email = form.email.data
            pwd = form.password.data
            cpwd = form.confirm_password.data

            if pwd != cpwd:
                flash('Passwords do not match')

            else:
                new_user = User(
                    username=uname,
                    email=email,
                    password=bcrypt.generate_password_hash(pwd)
                )

                db.session.add(new_user)
                db.session.commit()
                flash(f'Your account has been created!', 'success')
                return redirect(url_for('login'))

        except Exception:
            flash(' Username already exists ', 'danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')
        
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            hashed_pwd = bcrypt.check_password_hash(user.password, form.password.data)

            if user and hashed_pwd:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                # return redirect(next_page) if next_page else redirect(url_for('home'))
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))

            else:
                flash(f'Invalid credentials', 'danger')
        
        except Exception as e:
            flash(e, 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')