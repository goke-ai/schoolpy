import pytest

from werkzeug.security import check_password_hash, generate_password_hash

from flask import g, session
from school.models import Post, User, db

from conftest import init, close


def test_user_repl(load_db):
    load_db()

    user = User(name='test', email='test@ark.com',
                password=generate_password_hash('test'))
    
    assert repr(user) == "User('test')"


def test_post_repl(load_db):
    load_db()

    post = Post(title='test title', body='post body test')
    
    assert repr(post) == "Post('test title')"
