import os
from flask import Flask


def new_web_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/ping")
    def hello() -> str:
        # web application reachability check
        return "pong"

    return new_web_app
