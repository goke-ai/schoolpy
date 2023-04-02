import os

from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'school-raw-dev.sqlite'),
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
    # # db sqlite
    # from . import db
    # db.init_app(app)

    # sqlalchemy
    from school.models import db, migrate
    db.init_app(app)

    # migrate
    migrate.init_app(app, db)

    # from school.database import init_app  # , db_session
    # init_app(app)

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()

    # blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
