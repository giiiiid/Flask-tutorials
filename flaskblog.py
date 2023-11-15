from flask import Flask, render_template, url_for, flash, request, redirect
from forms import *

# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '964565dbc835b0ed7dbefe7248cffbcf'


# views/logic
@app.route('/')
def hello():
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


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)
