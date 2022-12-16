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

bp = Blueprint("groups", __name__, url_prefix="/groups")


@bp.route("/select", methods=("GET", "POST"))
def select():
    """Select a user"""
    if request.method == "POST":
        print(request.form)
        user_id = request.form["user_id"]
        error = None

        # Check inputs
        if "" in [
            user_id,
        ]:
            error = "All fields are required."
        else:
            return redirect(url_for("groups.manage"))
        flash(error)

    return render_template("/groups/select.html")


@bp.route("/manage", methods=("GET", "POST"))
def manage():
    error = None
    if request.method == "POST":
        print(request.form.getlist("groups"))
        user_id = g.user["user_id"]

        if "" in user_id:
            error = "Fields cannot be empty."

        if not error:
            statement = "SELECT n.group_name FROM user_groups g\
                     LEFT JOIN users u ON g.user_id = u.user_id\
                     LEFT JOIN groups n ON n.group_id = g.group_id\
                     WHERE u.user_id = ?"
            g.groups = [
                x[0] for x in get_database().execute(statement, (user_id,)).fetchall()
            ]  # Covert row to a list
            print(g.groups)

        flash(error)

    return render_template("/groups/manage.html")


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
        print(g.groups)
        if "managers" not in g.groups:
            return redirect(url_for("posts.index"))
        g.users = (
            get_database()
            .execute(
                "SELECT user_id, user_login FROM users ORDER BY user_id ASC",
            )
            .fetchall()
        )




#  select u.user_login, n.group_name  from user_groups g LEFT JOIN users u ON g.user_id = u.user_id LEFT JOIN groups n ON n.group_id = g.group_id WHERE u.user_login = "moo@cow.com";
# moo@cow.com|chatterboxes
# select *  from user_groups g LEFT JOIN users u ON g.user_id = u.user_id LEFT JOIN groups n ON n.group_id = g.group_id;
# 1|3|2|3|moo@cow.com|pbkdf2:sha256:260000$1gCdVwqWLO1dGEVmT3SjAD3wlABzDj7l$c28d32a34af32c6a8f449c190e166d406ef428b2150550832292b76fca8fd274|moo|cow|2022-12-13 15:52:08|2022-12-14 14:08:35.578991|enabled|2|chatterboxes
# 2|3|3|3|moo@cow.com|pbkdf2:sha256:260000$1gCdVwqWLO1dGEVmT3SjAD3wlABzDj7l$c28d32a34af32c6a8f449c190e166d406ef428b2150550832292b76fca8fd274|moo|cow|2022-12-13 15:52:08|2022-12-14 14:08:35.578991|enabled|3|natterers

# add user to group
# INSERT INTO user_groups (user_id, group_id) VALUES (2,3);
# INSERT INTO groups (group_name) VALUES ("natterers");
# group id 1 is managers.

# select n.group_name  from user_groups g LEFT JOIN users u ON g.user_id = u.user_id LEFT JOIN groups n ON n.group_id = g.group_id WHERE u.user_id=3;
# chatterboxes
# natterers


def login_required(view):
    """Login is required for all views here"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
