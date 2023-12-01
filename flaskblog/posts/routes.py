from flask import Blueprint, redirect, render_template, request, flash, abort, url_for
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.posts.forms import PublishForms
from flaskblog.models import Post
posts = Blueprint('posts', __name__)


@posts.route('/publish', methods=['POST', 'GET'])
@login_required
def publish():
    form = PublishForms()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('publish.html', form=form, legend='Publish a Post')


@posts.route('/publish/<int:id>', methods=['GET'])
@login_required
def read_post(id):
    post = Post.query.get_or_404(id)
    return render_template('read-post.html', post=post)


@posts.route('/publish/<int:id>/update', methods=['GET','POST'])
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


@posts.route('/publish/<int:id>/delete', methods=['GET', 'POST'])
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

