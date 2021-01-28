DROP TABLE IF EXISTS athletes;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS games_cities;
DROP TABLE IF EXISTS ages;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS medals;
DROP TABLE IF EXISTS nocs;
DROP TABLE IF EXISTS athletes_nocs;


CREATE TABLE athletes (
    id SERIAL,
    full_name text,
    sex text,
    height float,
    weights float
);

CREATE TABLE games (
    id SERIAL,
    games text,
    game_year integer,
    season text
);

CREATE TABLE cities (
    id SERIAL,
    city_name text
);

CREATE TABLE games_cities (
    game_id integer,
    city_id integer
);

CREATE TABLE ages (
    id SERIAL,
    athlete_id integer,
    game_id integer,
    age integer
);

CREATE TABLE events (
    id SERIAL,
    event_name text,
    sport text
);

CREATE TABLE medals (
    id SERIAL,
    athlete_id integer,
    game_id integer,
    event_id integer,
    medal text
);

CREATE TABLE nocs (
    id SERIAL,
    noc_name text,
    region text,
    notes text
);

CREATE TABLE athletes_nocs (
    athlete_id integer,
    noc_id integer
);

\copy athletes from 'athletes.csv' DELIMITER ',' CSV NULL AS 'NA'
\copy games from 'games.csv' DELIMITER ',' CSV NULL AS 'NA'
\copy events from 'events.csv' DELIMITER ',' CSV NULL AS 'NA'
\copy cities from 'cities.csv' DELIMITER ',' CSV NULL AS 'NA'
\copy nocs from 'nocs.csv' DELIMITER ',' CSV NULL AS ''
\copy games_cities from 'games_cities.csv' DELIMITER ',' CSV NULL AS ''
\copy athletes_nocs from 'athletes_nocs.csv' DELIMITER ',' CSV NULL AS ''
\copy ages from 'ages.csv' DELIMITER ',' CSV NULL AS 'NA'
\copy medals from 'medals.csv' DELIMITER ',' CSV NULL AS 'NA'

