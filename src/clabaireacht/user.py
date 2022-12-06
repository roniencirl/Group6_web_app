import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/user')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('registration.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('login.html')