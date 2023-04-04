import pytest

from flask import g, session
from school.models import Post, User, db

from conftest import init, close


def test_register(client, app, load_db):
    load_db()

    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register', data={'username': 'aaaa',
                                'email': 'aaaa@test.com',
                                'password': 'aaa',
                                'confirm': 'aaa',
                                }
    )

    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert db.session.execute(db.select(User).filter_by(
            name='aaaa')).scalar() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'confirm', 'message'), (
    ('', '','','', b'between 4 and 25 characters'),
    # ('a', '', b'Password is required.'),
    ('test1', 'test1@test.com', 'test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, email, password, confirm, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password,
              'email': email, 'confirm': confirm}
    )
    assert message in response.data


def test_login(client, auth, load_db):
    load_db()

    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.name == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message, load_db):
    load_db()

    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth, load_db):
    load_db()

    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
