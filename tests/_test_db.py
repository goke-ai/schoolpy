import pytest
from school.models import db


# def test_get_close_db(app):
#     with app.app_context():
#         assert db is app.()

#     with pytest.raises(sqlite3.ProgrammingError) as e:
#         db.execute('SELECT 1')

#     assert 'closed' in str(e.value)


# def test_init_db_command(runner, monkeypatch):
#     class Recorder(object):
#         called = False

#     def fake_init_db():
#         Recorder.called = True

#     monkeypatch.setattr('school.db.init_db', fake_init_db)
#     result = runner.invoke(args=['init-db'])
#     assert 'Initialized' in result.output
#     assert Recorder.called
