from flask import Blueprint, render_template,request
from flaskblog.models import Post
from flask_login import login_required
main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', title='FlaskBlog', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')