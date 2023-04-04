import functools

from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
)
import flask
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from school.forms import RegistrationForm

from school.models import User, db
from school.util import is_safe_url

bp = Blueprint('auth', __name__, url_prefix='/auth')


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login', next=request.url))

#         return view(*args, **kwargs)

#     return wrapped_view


# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = db.session.execute(db.select(User).filter_by(
#             id=user_id)).scalar()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    error = None

    form = RegistrationForm(request.form)

    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        try:
            user = User(name=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data))

            db.session.add(user)
            db.session.commit()

            flash('Thanks for registering')

        except Exception as e:
            error = f"User {form.username.data} is already registered."
        else:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True  # if request.form.get('remember') else False

        error = None

        user = db.session.execute(
            db.select(User).filter_by(name=username)).scalar()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            # session.clear()
            # session['user_id'] = user.id
            login_user(user, remember=remember)

            flask.flash('Logged in successfully.')
            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)

            if next is None or not next.startswith('/'):
                next = url_for('index')

            return redirect(next)

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    # session.clear()
    logout_user()
    return redirect(url_for('index'))
