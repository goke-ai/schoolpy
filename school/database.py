import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database_url = 'sqlite:///test.db'
engine = create_engine('sqlite:///test.db')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine
                                         ))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(database_url):

    engine = create_engine(database_url)

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import school.models
    Base.metadata.create_all(bind=engine)


def init_app(app):

    database_url = app.config["SQLALCHEMY_DATABASE_URI"]

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    init_db(database_url)
