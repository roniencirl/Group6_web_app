import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from werkzeug.security import check_password_hash, generate_password_hash

from clabaireacht.database import get_database

bp = Blueprint("auth", __name__, url_prefix="/user")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        db = get_database()  # pylint: disable=invalid-name
        error = None

        if None in [
            username,
            password,
            firstname,
            lastname,
            email,
        ]:
            error = "All fields are required."

        # TODO: sanitize and validate.

        if error is None:
            try:
                # Salt length increased and pepper added
                statement = "INSERT INTO users (user_login,\
                                        user_password,\
                                        user_firstname,\
                                        user_lastname,\
                                        user_email,\
                                        user_status )\
                                VALUES (?, ?, ?, ?, ?, ?)"

                db.execute(
                    statement,
                    (
                        username,
                        generate_password_hash(
                            current_app.config["PW_PEPPER_SECRET"] + password,
                            salt_length=32,
                        ),
                        firstname,
                        lastname,
                        email,
                        "enabled",
                    ),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("registration.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html")
