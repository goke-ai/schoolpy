from datetime import datetime
import os

from werkzeug.security import generate_password_hash

import pytest
from school import create_app
from school.models import Post, User, db


def init(app):
    with app.app_context():
        db.create_all()

        user = User(name="test",
                    email='test@ark.com',
                    password=generate_password_hash('test'))

        other = User(name="other",
                     email='other@ark.com',
                     password=generate_password_hash('other'))

        db.session.add(user)
        db.session.add(other)
        db.session.commit()

        post = Post(author_id=user.id,
                    title='test title',
                    body='test\nbody',
                    created=datetime(2018, 1, 1, 0, 0, 0)
                    )
        db.session.add(post)
        db.session.commit()


def close(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def load_db(app):
    def _make_db():
        init(app)

    yield _make_db

    close(app)


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('TEST_DATABASE_URL') or
        'sqlite:///' + os.path.join('school-test.sqlite'),
        'WTF_CSRF_ENABLED':False
    })

    with app.app_context():
        # init(app)
        pass

    yield app

    with app.app_context():
        close(app)
        pass


@pytest.fixture
def client(app):
    return app.test_client(use_cookies=True)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
