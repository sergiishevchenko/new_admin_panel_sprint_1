import datetime

from logger import get_logger
from models import T, Data
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values
from typing import Iterator


logger = get_logger(__name__)


class PostgresSaver:
    '''Method for saving data from SQLite DB to PostgreSQL DB.'''
    def __init__(self, connection: _connection, page_size: int):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.page_size = page_size

    def save_current_table(self, table_name: str, data: Iterator[T]):
        '''Saving current table method.
        Args:
            self: class instance
            table_name: current table name
            data: tables generator, Iterator - typing._GenericAlias, T - TypeVar(Declare type variable)
        '''
        # check running save_current_table() method
        logger.info('Running save_current_table() method')

        # set current time to start var
        start = datetime.datetime.now()

        # Execute a statement using :sql:`VALUES` with a sequence of parameters.
        execute_values(self.cursor, f"""INSERT INTO {table_name} VALUES %s ON CONFLICT (id) DO NOTHING;""", (
            row.values for row in data), page_size=self.page_size,)

        # display saving process time for every table
        logger.info('Saved data to {table_name} table for ' + str(datetime.datetime.now() - start))

    def save_all_data(self, data: Data):
        '''Saving all tables method.'''
        # check running save_all_data() method
        logger.info('Running save_all_data() method')

        for key, value in data.items():
            # call save_current_table() method for exact table
            # key - table name, value - generator SQLiteExtractor.extract_movie with data
            self.save_current_table(key, value)