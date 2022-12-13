import os
import tempfile
import pytest
from flask import current_app, g
from setup import _setup as clabaireacht_setup
from clabaireacht import create_app
from clabaireacht.database import get_database
from clabaireacht.utilities import sanitize_path

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")
    print(_data_sql)

print(os.getcwd())

db_fd, db_path = tempfile.mkstemp()
clabaireacht_setup(
    delete=False,
    db_path=db_path,
    schema_path="./src/schema",
    create_admin=False,
    production=False,
    db_name="testing",
)


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    # Create a testing db.
    clabaireacht_setup(
        delete=False,
        db_path=db_path,
        schema_path="./src/schema",
        create_admin=False,
        production=False,
        db_name="testing",
    )

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": sanitize_path(db_path) + "/testing.sqlite",
        }
    )

    with app.app_context():
        print(current_app.config)
        # load the test data
        get_database().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(sanitize_path(db_path) + "/testing.sqlite")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
