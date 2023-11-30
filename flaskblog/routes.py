import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, request, redirect, request, abort
from .models import User, Post
from .forms import (RegistrationForm, LoginForm, UpdateAccountForms, 
                    PublishForms, Request_ResetPassword_TokenForm, ResetPassword)
from flaskblog import app, bcrypt, db, login_user, mail
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message


@app.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', title='FlaskBlog', posts=posts)


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
            # yes_user = User.query.filter_by(username=form.username.data).exists()
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
            flash('User does not exist', 'danger')
    users = User.query.all()
    print(users)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/propic', image_fn)

    output_size = (125, 125)
    i = Image.open(form_image)
    i.resize(output_size)
    i.save(image_path)

    return image_fn


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForms()
    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            current_user.email = form.email.data

            if form.image.data:
                new_image = save_picture(form.image.data)
                current_user.image_file = new_image
                image_file = url_for('static', filename='propic/' + current_user.image_file)

            # update_user = User.query.update(username=current_user.username, email=current_user.email) throws an error(Exception)
            db.session.commit()
            flash('Your profile has successfully been updated', 'success')
            return redirect(url_for('account'))
        except Exception:
            flash('Username or email already exists', 'danger')
        

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename=f'propic/{current_user.image_file}')
        
    image_file = url_for('static', filename=f'propic/{current_user.image_file}')
    return render_template('user-acc.html', image_file=image_file, form=form)


@app.route('/profile/<int:id>', methods=['GET'])
@login_required
def user_profile(id):
    profile = User.query.get_or_404(id)
    image_file = url_for('static', filename='propic/' + profile.image_file)
    return render_template('user-profile.html', profile=profile, image_file=image_file)


@app.route('/publish', methods=['POST', 'GET'])
@login_required
def publish():
    form = PublishForms()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('publish.html', form=form, legend='Publish a Post')


@app.route('/publish/<int:id>', methods=['GET'])
@login_required
def read_post(id):
    post = Post.query.get_or_404(id)
    return render_template('read-post.html', post=post)


@app.route('/publish/<int:id>/update', methods=['GET','POST'])
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return redirect(url_for('read_post', id=post.id))

    form = PublishForms()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    elif form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('read_post', id=post.id))
    return render_template('publish.html', legend='Update a Post', form=form)


@app.route('/ipublish/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
        return redirect(url_for('read_post', id=post.id))

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted', 'success')
        return redirect(url_for('home'))
    return render_template('delete-post.html', post=post)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject='Password Reset request',
        recipients=[user.email],
        sender='noreply@gmail.com',
    )
    msg.body = f'''
    To reset your password, visit the following link: 
    {url_for('reset_pwd_token', token=token, _external=True)}

    If you did not request to reset your password, kindly ignore this email.
    '''
    mail.send(msg)

@app.route('/reset_password', methods=['GET','POST'])
def request_reset_pwd_token():
    form = Request_ResetPassword_TokenForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Check your email to reset your password','info')
            # send_reset_email(user)
        else:
            flash('Email does not exist', 'danger')
        # return redirect(url_for('reset_pwd_token'))
    return render_template('resetpwdtoken.html', form=form, legend='Reset Password')


@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_pwd_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expire token', 'warning')
        return redirect(url_for('request_reset_pwd_token'))
    form = ResetPassword()
    if form.validate_on_submit():
        pwd = form.password.data
        cpwd = form.confirm_pwd.data

        if pwd != cpwd:
            flash('Passwords do not match', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(pwd)
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('login'))

    return render_template('resetpwd.html', form=form, legend='Reset Password')