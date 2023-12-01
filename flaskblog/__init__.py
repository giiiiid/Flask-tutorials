from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# configuration
app = Flask(__name__)
app.config.from_object(Config)
# database configuration
db = SQLAlchemy(app)

# authentication configuration
bcrypt = Bcrypt(app)
login_user = LoginManager(app)
login_user.login_view = 'users.login'
login_user.login_message_category = 'info'

# mail configuration

mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)