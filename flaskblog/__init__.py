from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# database configuration
db = SQLAlchemy()

# authentication configuration
bcrypt = Bcrypt()
login_user = LoginManager()
login_user.login_view = 'users.login'
login_user.login_message_category = 'info'

# mail configuration
mail = Mail()


def create_app(confg_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    db.init_app(app)
    bcrypt.init_app(app)
    login_user.init_app(app)
    mail.init_app(app)

    return app