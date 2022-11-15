import os
from flask import Flask

USERDB_SECRET = None
POSTDB_SECRET = None

# flask application factory
def create_app():
    clabaireact = Flask(__name__, instance_relative_config=True)
    print(__name__)
    clabaireact.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(clabaireact.instance_path, "flaskr.sqlite"),
    )
    clabaireact.config.from_envvar("USERDB_SECRET", silent=True)
    clabaireact.config.from_envvar("POSTDB_SECRET", silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(clabaireact.instance_path, mode=0o600)
    except OSError:
        pass

    @clabaireact.route("/ping")
    def hello() -> str:
        # web application reachability check
        return "pong"

    return clabaireact
