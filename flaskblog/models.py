from flaskblog import db, login_user
from datetime import datetime
from flask_login import UserMixin, LoginManager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

# Loading a user's id and logging it in
@login_user.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default-pic/default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)


    def get_reset_token(self, expires=30):
        s = Serializer(current_app.config['SECRET_KEY'], expires)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id =  s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.date})'