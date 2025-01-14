-- CREATE IF NOT EXISTS KEYSPACE ork_cinema
--   WITH REPLICATION = { 
--    'class' : 'SimpleStrategy', 
--    'replication_factor' : 1 
--   };
;

DROP TABLE IF EXISTS ork_cinema.cities;

CREATE TABLE ork_cinema.cities (
  id UUID,
  name TEXT,
  add_info TEXT,
  PRIMARY KEY (id)
);

-- Poznań 624a9fe7-069a-4040-9a3f-025fd3e14166
-- Warszawa e7a54e11-ce61-4350-aa69-6b6a8bc913ef

INSERT INTO ork_cinema.cities (id, name, add_info) VALUES (624a9fe7-069a-4040-9a3f-025fd3e14166, 'Poznań', 'Wielkopolska');
INSERT INTO ork_cinema.cities (id, name, add_info) VALUES (e7a54e11-ce61-4350-aa69-6b6a8bc913ef, 'Warszawa', 'Mazowsze');

CREATE TABLE ork_cinema.cinemas (
  id UUID,
  name TEXT,
  PRIMARY KEY (id, name)
);

SELECT * FROM ork_cinema.cities;

INSERT INTO ork_cinema.cinemas (id, name) VALUES (uuid(), 'Multikino');
INSERT INTO ork_cinema.cinemas (id, name) VALUES (uuid(), 'Cinema City');

CREATE TABLE ork_cinema.films (
  id UUID,
  film_name TEXT,
  PRIMARY KEY (id, film_name)
);

INSERT INTO ork_cinema.films (id, film_name) VALUES (uuid(), 'Matrix');
INSERT INTO ork_cinema.films (id, film_name) VALUES (uuid(), 'Pulp Fiction');

CREATE TABLE ork_cinema.films_by_city (
  city_id UUID,
  film_id UUID,
  film_name TEXT,
  PRIMARY KEY ((city_id), film_id)
);

CREATE TABLE ork_cinema.cinemas_by_film_city (
  city_id UUID,
  film_id UUID,
  film_name TEXT,
  cinema_id UUID,
  cinema_name TEXT,
  PRIMARY KEY ((film_id, city_id), cinema_id)
);

CREATE TABLE ork_cinema.timeslots_by_cinema_film (
  film_id UUID,
  film_name TEXT,
  cinema_id UUID,
  cinema_name TEXT,
  timeslot TIMESTAMP,
  PRIMARY KEY ((film_id, cinema_id, city_id), timeslot)
);

CREATE TABLE ork_cinema.seats_by_cinema_film_timeslot (
  cinema_id UUID,
  film_id UUID,
  timeslot TIMESTAMP,
  seat_number INT,
  is_booked BOOLEAN,
  PRIMARY KEY ((cinema_id, film_id, timeslot), seat_number)
);

CREATE TABLE ork_cinema.booked_seats_by_user (
  user_name TEXT,
  cinema_id UUID,
  film_id UUID,
  timeslot TIMESTAMP,
  seat_number INT,
  PRIMARY KEY ((user_name), cinema_id, film_id, timeslot, seat_number)
);

SELECT * FROM ork_cinema.seats_by_cinema_film_timeslot
WHERE cinema_id = 55309a44-4009-4504-9c52-eddb238efc65 
AND film_id = a62a46fc-5c37-4db2-a994-ed0290d6cc14;

SELECT * FROM ork_cinema.seats_by_cinema_film_timeslot
WHERE cinema_id = 55309a44-4009-4504-9c52-eddb238efc65 
AND film_id = a62a46fc-5c37-4db2-a994-ed0290d6cc14 
AND timeslot = '2021-10-10T10:00:00.000Z';

BEGIN BATCH
  UPDATE 
  ork_cinema.seats_by_cinema_film_timeslot 
  SET is_booked = TRUE, 
  user_name = 'stas' 
  WHERE cinema_id = 55309a44-4009-4504-9c52-eddb238efc65 
  AND film_id = a62a46fc-5c37-4db2-a994-ed0290d6cc14 
  AND timeslot = '2021-10-10T12:00:00.000Z'
  AND seat_number = 6 
  IF is_booked = FALSE AND user_name = NULL;

  UPDATE 
  ork_cinema.seats_by_cinema_film_timeslot 
  SET is_booked = FALSE, 
  user_name = NULL
  WHERE cinema_id = 55309a44-4009-4504-9c52-eddb238efc65 
  AND film_id = a62a46fc-5c37-4db2-a994-ed0290d6cc14 
  AND timeslot = '2021-10-10T10:00:00.000Z'
  AND seat_number = 6 
  IF is_booked = TRUE AND user_name = 'stas';
APPLY BATCH;