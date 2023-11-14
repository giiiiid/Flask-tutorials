from flask import Flask, render_template
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

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)






if __name__ == '__main__':
    app.debug = True
    app.run()
