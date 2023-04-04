from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text

from . import db

# CREATE TABLE user (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name TEXT UNIQUE NOT NULL,
#   password TEXT NOT NULL
# );


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(128), unique=True)
    password = Column(Text, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # self.name = name
        # self.password = password

    def __repr__(self):
        return f'User({self.name!r})'


# CREATE TABLE post (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   author_id INTEGER NOT NULL,
#   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   title TEXT NOT NULL,
#   body TEXT NOT NULL,
#   FOREIGN KEY (author_id) REFERENCES user (id)
# );

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        # self.author_id = author_id
        # self.created = created
        # self.title = title
        # self.body = body

    def __repr__(self):
        return f'Post({self.title!r})'
