import os
from flask import Flask, render_template
from . import database
from . import posts
from . import auth

# Load environment variables
PW_PEPPER_SECRET = str(os.environ.get("PW_PEPPER_SECRET", ""))
SECRET_KEY = str(os.environ.get("SECRET_KEY", "dev"))
MAX_CONTENT_LENGTH = int(
    os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
)  # 16 MB


# flask application factory
def create_app(test_config=None):
    clabaireacht = Flask(__name__, instance_relative_config=True)
    print(__name__)

    clabaireacht.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=os.path.join(clabaireacht.instance_path, "clabaireacht.sqlite"),
        PW_PEPPER_SECRET=PW_PEPPER_SECRET,
        MAX_CONTEXT_LENGTH=MAX_CONTENT_LENGTH,
    )

    # Load production configuration, if it exists, when not testing
    if test_config is None:
        clabaireacht.config.from_pyfile("../config.py", silent=True)
    else:
        clabaireacht.config.from_mapping(test_config)

    print(clabaireacht.config)
    # ensure the instance folder exists
    try:
        os.makedirs(clabaireacht.instance_path, mode=0o700)
    except OSError:
        pass

    @clabaireacht.route("/ping")
    def pong() -> str:
        """ " Web application reachability check"""
        return "pong"

    clabaireacht.register_blueprint(auth.bp)
    clabaireacht.register_blueprint(posts.bp)

    return clabaireacht
