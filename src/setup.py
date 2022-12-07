import sqlite3
import os, errno
import click
from clabaireacht.utilities import sanitize_path

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
def setup(delete: bool, db_path: str, schema_path: str):
    clean_db_path = sanitize_path(db_path)
    clean_schema_path = sanitize_path(schema_path)

    if delete:
        delete_db(f"{clean_db_path}/{DATABASE}.sqlite")
        click.echo(f"{clean_db_path}/{DATABASE}.sqlite Deleted.")

    try:
        os.makedirs(f"{clean_db_path}", mode=0o700)
    except OSError:
        pass

    database = sqlite3.connect(f"{clean_db_path}/{DATABASE}.sqlite")

    try:
        load_schema(f"{clean_schema_path}/{DATABASE}.sql", database)
    except Exception as e:
        print(f"Failed to load schema. {e}")
        raise
    click.echo(f"Schema loaded to database: {clean_db_path}/{DATABASE}.sqlite")

    database.close()
    return


if __name__ == "__main__":
    setup()  # pylint: disable=no-value-for-parameter
