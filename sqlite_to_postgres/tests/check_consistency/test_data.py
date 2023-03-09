import sqlite3
import psycopg2

from contextlib import contextmanager
from dotenv import load_dotenv
from dataclasses import fields
from psycopg2.extras import DictCursor
from utils import get_db_creds, get_models


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def test_tables_data_integrity():
    '''Data integrity checking between each pair of tables in SQLite and Postgres.
       It is enough to check the number of records in each table.
    '''

    # Connection to PostgreSQL and SQLite DBs
    with (conn_context(**db_creds['sqlite']) as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn):
        for table_name in models:
            curs = sqlite_conn.cursor()
            sqlite_rows_quantity = curs.execute(
                f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]

            cursor = pg_conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM content.{table_name};')
            postgres_rows_quantity = cursor.fetchone()[0]

            assert sqlite_rows_quantity == postgres_rows_quantity, \
                (f'Record quantity in {table_name} PostgreSQL does not equal to SQLite.')


if __name__ == '__main__':
    # upload environment variables
    load_dotenv()

    # call method for getting databases creds
    db_creds = get_db_creds()

    # call method for getting list of models
    models = get_models()

    # Tests
    # call the method for checking data integrity
    test_tables_data_integrity()