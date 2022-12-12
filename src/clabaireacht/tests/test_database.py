import sqlite3
import pytest
from flask import current_app
from clabaireacht.database import get_database, close_database


def test_get_close_db(app):
    with app.app_context():
        db = get_database()
        assert db is get_database()

    close_database()        
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


"""
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("clabaireacht.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
"""
