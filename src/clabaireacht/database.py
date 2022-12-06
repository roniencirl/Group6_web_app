import sqlite3
import click
from flask import current_app, g


def get_database():
    """Open database into the current application context."""
    if "database" not in g:
        print(current_app.config["DATABASE"])
        g.database = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row
    return g.database


def close_database(e=None):
    """Close the database if open."""
    database = g.pop("database", None)
    if database is not None:
        database.close()


def init_app(app):
    app.teardown_appcontext(close_database)
