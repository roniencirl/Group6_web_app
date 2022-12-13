# Utility functions for sanitisation, parsing, security etc.
import os
from email_validator import validate_email, EmailNotValidError
from password_strength import PasswordStats


def sanitize_path(path: str) -> str:
    """Returns a sanitized path which is relative to current directory and does not include directory traversal"""
    return os.path.relpath(os.path.normpath(os.path.join("/", path)), "/")


def valid_email(email: str, mx_check: bool = False) -> bool:
    """Validates an email address is correct."""
    try:
        validation = validate_email(
            email, check_deliverability=mx_check, allow_smtputf8=False
        )
    except EmailNotValidError as e:
        print(str(e))
        return False
    return True


def check_password_strength(password: str, score: float = 0.66):
    stats = PasswordStats(password).strength()
    print(stats)
    if stats >= score:
        return True
    return False
