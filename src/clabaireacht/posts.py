from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)

from clabaireacht.database import get_database
from clabaireacht.auth import login_required


bp = Blueprint("posts", __name__)


@bp.route("/")
def index():
    db = get_database()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, user_login"
        " FROM posts p JOIN users u ON p.author_id = u.user_id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("posts/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        # TODO:  Sanitise the form input.

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            database = get_database()

            user_id = g.user["user_id"]

            database.execute(
                "INSERT INTO posts (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, user_id),
            )
            database.commit()
            return redirect(url_for("posts.index"))

    return render_template("posts/create.html")
