# Utility functions for sanitisation, parsing, security etc.
import os


def sanitize_path(path: str):
    """Returns a sanitized path which is relative to current directory and does not include directory traversal"""
    return os.path.relpath(os.path.normpath(os.path.join("/", path)), "/")