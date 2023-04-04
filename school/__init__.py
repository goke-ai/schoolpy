import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
# login-manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
    
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or
        'sqlite:///' + os.path.join(app.instance_path, 'school-dev.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!. Welcome to the School App!!'

    # database
    # sqlalchemy
    # from school.models import db, migrate
    db.init_app(app)

    # migrate
    migrate.init_app(app, db)
    
    # login-manager
    login_manager.init_app(app)

    from school.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        sql = db.select(User).where(User.id == int(user_id))
        user = db.session.execute(sql).scalar()
        return user


    # blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
