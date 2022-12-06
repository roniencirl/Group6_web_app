from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from clabaireacht.database import get_database


bp = Blueprint("posts", __name__)


@bp.route("/")
def index():
    database = get_database()
    print(type(database))
    print(database)
    posts = database.execute(
        "SELECT p.id, title, body, created, author_id, user_login"
        " FROM posts p JOIN users u ON p.author_id = u.user_id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("posts/index.html", posts=posts)
