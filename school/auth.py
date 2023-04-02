import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from school.db import get_db
from school.models import User, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()

        g.user = db.session.execute(db.select(User).filter_by(
            id=user_id)).scalar_one()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # db = get_db()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # db.execute(
                #     "INSERT INTO user (username, password) VALUES (?, ?)",
                #     (username, generate_password_hash(password)),
                # )
                # db.commit()

                user = User(name=username,
                            email=username,
                            password=generate_password_hash(password))

                db.session.add(user)
                db.session.commit()

            except Exception as e:
                error = f"User {username} is already registered. {e}"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # db = get_db()

        error = None

        # user = db.execute(
        #     'SELECT * FROM user WHERE username = ?', (username,)
        # ).fetchone()

        user = db.session.execute(
            db.select(User).filter_by(name=username)).scalar_one()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(
            # user['password']
            user.password,
            password
        ):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # session['user_id'] = user['id'] or user.id
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))