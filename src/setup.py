import sqlite3
import os, errno
import click
import configparser
from clabaireacht.utilities import sanitize_path
import secrets

DATABASE = "clabaireacht"


def delete_db(path: str):
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def load_schema(path: str, database: sqlite3.Connection):
    with open(path, "r") as file:
        database.executescript(file.read())


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
@click.option(
    "--create-admin",
    type=bool,
    is_flag=True,
    default=False,
    help="Prompt to create/update administrator user.",
)
@click.option(
    "--production",
    type=bool,
    is_flag=True,
    default=False,
    help="Setup a strong secret key to protect session cookies.",
)
def setup(
    delete: bool, db_path: str, schema_path: str, create_admin: bool, production: bool
):
    return _setup(
        delete=delete,
        db_path=db_path,
        schema_path=schema_path,
        create_admin=create_admin,
        production=production,
    )


def _setup(
    delete: bool,
    db_path: str,
    schema_path: str,
    create_admin: bool,
    production: bool,
    db_name: str = DATABASE,
):

    clean_db_path = sanitize_path(db_path)
    clean_schema_path = sanitize_path(schema_path)

    if production:
        secret = f'SECRET_KEY = "{secrets.token_hex(32)}"'
        with open("config.py", "w") as config:
            config.write(secret)
        config.close()
        return

    if delete:
        delete_db(f"{clean_db_path}/{db_name}.sqlite")
        click.echo(f"{clean_db_path}/{db_name}.sqlite Deleted.")

    try:
        os.makedirs(f"{clean_db_path}", mode=0o700)
    except OSError:
        pass

    database = sqlite3.connect(f"{clean_db_path}/{db_name}.sqlite")

    try:
        load_schema(f"{clean_schema_path}/{DATABASE}.sql", database)
    except Exception as e:
        print(f"Failed to load schema. {e}")
        raise
    click.echo(f"Schema loaded to database: {clean_db_path}/{db_name}.sqlite")

    if create_admin:
        # search for existing admin user (should be uid 0)
        click.echo("Create admin")
        # click.prompt

    database.close()
    return


if __name__ == "__main__":
    setup()  # pylint: disable=no-value-for-parameter
