import os
import psycopg2
import sqlite3

from dotenv import load_dotenv
from logger import get_logger
from logging import Logger

from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from utils import get_db_creds


def load_from_sqlite(logger: Logger, connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres
    Args:
        logger: логгер
        connection: подключение к SQLite
        pg_conn: подключение к PostgreSQL
        page_size: пачка данных
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

    # define logger
    logger = get_logger(__name__)

    # databases creds
    db_creds = get_db_creds()

    # connection to DBs
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**db_creds['psql'], cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(logger, sqlite_conn, pg_conn)
