import sqlite3
import click
import os, errno

USER_DB = "users"
CONTENT_DB = "posts"


def sanitize_path(path: str):
    """Returns a sanitized path which is relative to current directory and does not include directory traversal"""
    return os.path.relpath(os.path.normpath(os.path.join("/", path)), "/")


def delete_db(path: str):
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def load_schema(path: str, db: sqlite3.Connection):
    with open(path, "r") as file:
        db.executescript(file.read())


@click.command()
@click.option(
    "--delete",
    type=bool,
    is_flag=True,
    default=False,
    help="Delete user and content databases and recreate.",
)
@click.option("--db-path", type=str, default="./instance", help="Path to database.")
@click.option("--schema-path", type=str, default="./schema", help="Path to database.")
def setup(delete: bool, db_path: str, schema_path: str):
    clean_db_path = sanitize_path(db_path)
    clean_schema_path = sanitize_path(schema_path)

    if delete:
        delete_db(f"{clean_db_path}/{USER_DB}.sqlite")
        delete_db(f"{clean_db_path}/{CONTENT_DB}.sqlite")
        click.echo(f"{clean_db_path}/{USER_DB}.sqlite Deleted.")
        click.echo(f"{clean_db_path}/{CONTENT_DB}.sqlite Deleted.")

    user_db = sqlite3.connect(f"{clean_db_path}/{USER_DB}.sqlite")
    content_db = sqlite3.connect(f"{clean_db_path}/{CONTENT_DB}.sqlite")

    try:
        load_schema(f"{clean_schema_path}/{USER_DB}.sql", user_db)
        load_schema(f"{clean_schema_path}/{CONTENT_DB}.sql", content_db)
    except Exception as e:
        print(f"Failed to load schema. {e}")
        raise
    click.echo("Schema loaded for USER and CONTENT DB.")

    user_db.close()
    content_db.close()
    return


if __name__ == "__main__":
    setup()  # pylint: disable=no-value-for-parameter
