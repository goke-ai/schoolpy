from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

# from school.auth import login_required
from school.models import Post, User, db

bp = Blueprint('blog', __name__)


def get_post(id, check_author=True) -> Post:
    post = db.get_or_404(Post, id)

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/')
def index():
    posts = db.session.execute(
        db.select(Post).order_by(Post.created)).scalars()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(author_id=g.user.id,
                        title=title, body=body)
            db.session.add(post)
            db.session.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('blog.index'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('blog/profile.html', name=current_user.name)
