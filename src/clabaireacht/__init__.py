import os
from flask import Flask, render_template
from . import database
from . import posts
from . import user

DB_SECRET = None
POSTDB_SECRET = None

# flask application factory
def create_app():
    clabaireacht = Flask(__name__, instance_relative_config=True)
    print(__name__)
    clabaireacht.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(clabaireacht.instance_path, "clabaireacht.sqlite"),
    )
    clabaireacht.config.from_envvar("DB_SECRET", silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(clabaireacht.instance_path, mode=0o700)
    except OSError:
        pass

    @clabaireacht.route("/ping")
    def pong() -> str:
        """ " Web application reachability check"""
        return "pong"

    clabaireacht.register_blueprint(user.bp)
    clabaireacht.register_blueprint(posts.bp)

    return clabaireacht
