CREATE SCHEMA IF NOT EXISTS content;

ALTER ROLE app SET search_path TO content,public;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    created timestamp with time zone,
    genre_id uuid,
    film_work_id uuid,
    CONSTRAINT genre_id
      FOREIGN KEY(id)
	  REFERENCES genre(id),
    CONSTRAINT film_work_id
      FOREIGN KEY(id)
	  REFERENCES film_work(id)
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    created timestamp with time zone,
    role TEXT,
    person_id uuid,
    film_work_id uuid,
    CONSTRAINT person_id
      FOREIGN KEY(id)
	  REFERENCES person(id),
    CONSTRAINT film_work_id
      FOREIGN KEY(id)
	  REFERENCES film_work(id)
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);
CREATE INDEX film_work_title_idx ON content.film_work(title);

CREATE INDEX person_full_name_idx ON content.person(full_name);

CREATE INDEX genre_name_idx ON content.genre(name);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE INDEX film_work_genre_idx ON content.genre_film_work(film_work_id, genre_id);

