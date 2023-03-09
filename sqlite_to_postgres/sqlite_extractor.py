import datetime
import sqlite3

from logger import get_logger
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork, T
from typing import Type


logger = get_logger(__name__)


class SQLiteExtractor:
    '''Method for extraction data from SQLite DB.'''
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.connection = sqlite_conn
        self.cursor = self.connection.cursor()

    def extract_movie(self, table_name: str, model: Type[T]):
        '''Extraction data method from one model.
        Args:
            self: class instance
            table_name: current table name
            model: class 'type' (class 'models.TableName'), T - TypeVar (Declare type variable)
        '''
        logger.info('Running extract_movie() method.')
        for row in self.cursor.execute(f"SELECT * from {table_name}"):
            yield model(*row)

    def extract_movies(self):
        '''All movies extraction method.'''
        logger.info('Running extract_movies() method')

        # set current time to start var
        start = datetime.datetime.now()

        extract_movies = {}
        # call extract_movie() method for every model
        extract_movies['film_work'] = self.extract_movie('film_work', FilmWork)
        extract_movies['person'] = self.extract_movie('person', Person)
        extract_movies['person_film_work'] = self.extract_movie(
            'person_film_work', PersonFilmWork)
        extract_movies['genre'] = self.extract_movie('genre', Genre)
        extract_movies['genre_film_work'] = self.extract_movie(
            'genre_film_work', GenreFilmWork)

        logger.info('Extracted movies for ' +
                    str(datetime.datetime.now() - start))

        return extract_movies
