import pytest
from clabaireacht.database import get_database


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={
            "username": "a@example.com",
            "password": "a",
            "firstname": "a",
            "lastname": "a",
        },
    )
    assert response.headers["Location"] == "/auth/login"

    app.app_context()
    with app.app_context():
        assert (
            get_database()
            .execute(
                "SELECT * FROM users WHERE user_login = 'a@example.com'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "firstname", "lastname", "message"),
    (
        ("", "b", "c", "d", b"All fields are required."),
        ("b@example.com", "", "c", "d", b"All fields are required."),
        ("c@example.com", "a", "", "d", b"All fields are required."),
        ("d@example.com", "a", "c", "", b"All fields are required."),
        ("test@example.com", "test", "c", "d", b"already registered"),
        ("test", "test", "c", "d", b"Please provide a valid email address."),
    ),
)
def test_register_validate_input(
    client, username, password, firstname, lastname, message
):
    response = client.post(
        "/auth/register",
        data={
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
        },
    )
    assert message in response.data
