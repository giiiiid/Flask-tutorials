from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '964565dbc835b0ed7dbefe7248cffbcf'
# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_user = LoginManager(app)

from . import routes