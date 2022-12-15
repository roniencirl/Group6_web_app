import os
import secrets
from datetime import timedelta
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from . import database
from . import posts
from . import auth

# Load environment variables
PW_PEPPER_SECRET = str(os.environ.get("PW_PEPPER_SECRET", ""))
SECRET_KEY = str(os.environ.get("SECRET_KEY", "dev"))
MAX_CONTENT_LENGTH = int(
    os.environ.get("MAX_CONTENT_LENGTH", 2 * 1024 * 1024)
)  # 2 MB max content upload size
PERMANENT_SESSION_LIFETIME = timedelta(
    minutes=int(os.environ.get("PERMANENT_SESSION_LIFETIME", "30"))
)  # Timeout after 30 mintues without an action
LOCK_ACCOUNT_DAYS = int(
    os.environ.get("LOCK_ACCOUNT_DAYS", "30")
)  # Lock inactive accounts after 30 days

csrf = CSRFProtect()

# flask application factory
def create_app(test_config=None):
    clabaireacht = Flask(__name__, instance_relative_config=True)
    print(__name__)
    csrf.init_app(clabaireacht)  # enable CSRF protection
    clabaireacht.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=os.path.join(clabaireacht.instance_path, "clabaireacht.sqlite"),
        PW_PEPPER_SECRET=PW_PEPPER_SECRET,
        MAX_CONTEXT_LENGTH=MAX_CONTENT_LENGTH,
        PERMANENT_SESSION_LIFETIME=PERMANENT_SESSION_LIFETIME,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        LOCK_ACCOUNT_DAYS=LOCK_ACCOUNT_DAYS,
        WTF_CSRF_SECRET_KEY=secrets.token_hex(
            32
        ),  # Random CSRF secret every execution.
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
