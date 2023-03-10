from logging import Logger
import os
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from logger import get_logger
from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor
from utils import get_db_creds


def load_from_sqlite(logger: Logger, connection: sqlite3.Connection, pg_conn: _connection):
    """Upload data method from SQLite to Postgres
    Args:
        logger: logger
        connection: connection to SQLite
        pg_conn: connection to PostgreSQL
        page_size: page size (record quantity)
    """
    postgres_saver = PostgresSaver(pg_conn, PAGE_SIZE)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)

    logger.info('Loading data from SQLite DB to PostgreSQL DB completed successfully!')


if __name__ == '__main__':
    # upload environment variables
    load_dotenv()

    # convert type of PAGE_SIZE from str to int
    PAGE_SIZE = int(os.environ.get('PAGE_SIZE'))

    logger = get_logger(__name__)

    # databases creds
    db_creds = get_db_creds()

    # connection to DBs
    with sqlite3.connect(**db_creds['sqlite_DB_NAME']) as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(logger, sqlite_conn, pg_conn)

    # close connections
    sqlite_conn.close()
    pg_conn.close()
