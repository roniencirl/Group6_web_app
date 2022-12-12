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
from clabaireacht.utilities import valid_email

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        db = get_database()  # pylint: disable=invalid-name
        error = None

        ### Check inputs
        print(type(username))
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

        # TODO: sanitize and validate.

        ####

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
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("/auth/registration.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # TODO: Sanitise
        error = None

        if not valid_email(email=username):
            error = "Please provide a valid email address."

        #
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
                print(user["user_password"])
                print(current_app.config["PW_PEPPER_SECRET"] + password)

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            print(session)
            return redirect(url_for("posts.index"))

        flash(error)

    return render_template("/auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_database()
            .execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            .fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("posts.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
