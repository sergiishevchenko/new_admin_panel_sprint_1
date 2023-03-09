from dataclasses import dataclass, field, astuple
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, Iterator, Optional, Tuple, TypeVar
from uuid import UUID


# T - Declare Type variable.
# Usage: T = TypeVar('T')  # Can be anything. Must be str or bytes. Bound to required class (Model)
T = TypeVar('T', bound='Model')
# Iterator - typing._GenericAlias. A generic version of collections.abc.Iterator.
Data = Dict[str, Iterator[T]]


@dataclass
class Model:
    '''Model dataclass.'''
    @property
    def values(self) -> Tuple[Any, ...]:
        return astuple(self)


@dataclass
class FilmType(str, Enum):
    '''FilmType dataclass.'''
    movie = 'movie'
    tv_show = 'tv_show'


@dataclass
class RoleType(str, Enum):
    '''RoleType dataclass.'''
    actor = 'actor'
    writer = 'writer'
    director = 'director'


@dataclass
class FilmWork(Model):
    '''FilmWork dataclass.'''
    id: UUID
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    file_path: Optional[str]
    rating: Optional[float]
    type: Optional[FilmType]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Person(Model):
    '''Person dataclass.'''
    id: UUID
    full_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PersonFilmWork(Model):
    '''PersonFilmWork dataclass.'''
    id: UUID
    person_id: UUID
    film_work_id: UUID
    role: Optional[RoleType]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Genre(Model):
    '''Genre dataclass.'''
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GenreFilmWork(Model):
    '''GenreFilmWork dataclass.'''
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created_at: datetime = field(default_factory=datetime.utcnow)
