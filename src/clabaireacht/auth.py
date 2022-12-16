""" Module containing authentication related actions"""
import functools
from datetime import datetime, timedelta
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
from clabaireacht.utilities import valid_email, check_password_strength

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        db = get_database()  # pylint: disable=invalid-name
        error = None

        ### Check inputs
        if "" in [
            username,
            password,
            firstname,
            lastname,
        ]:
            error = "All fields are required."

        # username must be an email address
        elif not valid_email(email=username):
            error = "Please provide a valid email address."
        # enforce password strength in production
        elif not current_app.config[
            "SECRET_KEY"
        ] == "dev" and not check_password_strength(password):
            error = "Weak password."
            del password  # best effort removal, python strings are immutable

        if error is None:
            try:
                # Salt length increased and pepper added
                statement = "INSERT INTO users (user_login,\
                                        user_password,\
                                        user_firstname,\
                                        user_lastname,\
                                        user_status )\
                                VALUES (?, ?, ?, ?, ?)"
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
                        "enabled",
                    ),
                )
                del password  # best effort removal, python strings are immutable
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("/auth/registration.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Login a user"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None

        if not valid_email(email=username):
            error = "Please provide a valid email address."
            del password  # best effort removal, python strings are immutable

        # Proceeed with Password check.
        if error is None:
            db = get_database()
            user = db.execute(
                "SELECT * FROM users WHERE user_login = ?", (username,)
            ).fetchone()
            if None in [user, password]:
                error = "Please provide an email address and password."
            elif not check_password_hash(
                user["user_password"], current_app.config["PW_PEPPER_SECRET"] + password
            ):
                error = "Incorrect email address or password."
            del password  # best effort removal, python strings are immutable

        # Check for last login time out to determine if account should be disabled.
        if error is None:
            print(user["user_last_login"])
            if user["user_last_login"] > (
                datetime.now()
                - timedelta(days=current_app.config["LOCK_ACCOUNT_DAYS"] * -1)
            ):
                # disable the account
                try:
                    statement = "UPDATE users SET user_status = ?\
                                WHERE user_id = ?"
                    db.execute(
                        statement,
                        (
                            "disabled",
                            user["user_id"],
                        ),
                    )
                    db.commit()
                    session.clear()
                    return redirect(url_for("posts.index"))
                except db.IntegrityError:
                    error = f"An error occured disabling {g.user['user_login']}."
                session.clear()
                return redirect(url_for("posts.index"))

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            # set the last login
            statement = """UPDATE users SET user_last_login = ? where user_id = ?"""
            time = datetime.now()
            db.execute(statement, (time, user["user_id"]))
            db.commit()
            print(session)
            return redirect(url_for("posts.index"))

        flash(error)

    return render_template("/auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """Load user session"""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_database()
            .execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            .fetchone()
        )
        statement = "SELECT n.group_name FROM user_groups g\
                     LEFT JOIN users u ON g.user_id = u.user_id\
                     LEFT JOIN groups n ON n.group_id = g.group_id\
                     WHERE u.user_id = ?"
        g.groups = [
            x[0] for x in get_database().execute(statement, (user_id,)).fetchall()
        ]  # Covert row to a list


@bp.route("/logout")
def logout():
    """Logout a user"""
    session.clear()
    return redirect(url_for("posts.index"))


@bp.route("/profile", methods=("GET", "POST"))
def profile():
    """Update a users profile"""
    if request.method == "POST":
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        db = get_database()  # pylint: disable=invalid-name
        error = None

        ### Check inputs
        if "" in [
            password,
            firstname,
            lastname,
        ]:
            error = "Fields cannot be empty."
        # enforce password strength in production
        elif not current_app.config[
            "SECRET_KEY"
        ] == "dev" and not check_password_strength(password):
            error = "Weak password."
            del password  # best effort removal, python strings are immutable

        if error is None:
            try:
                statement = "UPDATE users SET user_password = ?, \
                            user_firstname = ?,\
                            user_lastname = ? ,\
                            user_status = ?\
                            WHERE user_id = ?"

                db.execute(
                    statement,
                    (
                        generate_password_hash(
                            current_app.config["PW_PEPPER_SECRET"] + password,
                            salt_length=32,
                        ),
                        firstname,
                        lastname,
                        g.user["user_status"],
                        g.user["user_id"],
                    ),
                )
                del password  # best effort removal, python strings are immutable
                db.commit()
            except db.IntegrityError:
                error = f"An error occured updating {g.user['user_login']}."
            else:
                return redirect(url_for("auth.profile"))

        flash(error)

    return render_template("/auth/profile.html")


@bp.route("/deactivate", methods=("GET", "POST"))
def deactivate():
    """Disable or delete a users account"""
    if request.method == "POST":
        password = request.form["password"]
        action = request.form["disable"]
        db = get_database()  # pylint: disable=invalid-name
        error = None

        if not check_password_hash(
            g.user["user_password"],
            current_app.config["PW_PEPPER_SECRET"] + password,
        ):
            error = "Incorrect password."

        if error is None:
            if action == "deactivate":
                try:
                    statement = "UPDATE users SET user_status = ?\
                                WHERE user_id = ?"
                    db.execute(
                        statement,
                        (
                            "disabled",
                            g.user["user_id"],
                        ),
                    )
                    db.commit()
                    session.clear()
                    return redirect(url_for("posts.index"))
                except db.IntegrityError:
                    error = f"An error occured disabling {g.user['user_login']}."
            elif action == "delete":
                try:
                    statement = "DELETE FROM users WHERE user_id = ?"
                    db.execute(
                        statement,
                        (g.user["user_id"],),
                    )
                    statement = "DELETE FROM posts WHERE author_id = ?"
                    db.execute(
                        statement,
                        (g.user["user_id"],),
                    )
                    db.commit()
                    session.clear()
                    return redirect(url_for("posts.index"))
                except db.IntegrityError:
                    error = f"An error occured deleting {g.user['user_login']}."
            else:
                return redirect(url_for("auth.profile"))
        flash(error)

    return render_template("/auth/deactivate.html")


def login_required(view):
    """Login is required for all views here"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
