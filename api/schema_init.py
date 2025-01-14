import time

from cassandra.cluster import Cluster
from config import CassandraConfig

cassandra_config = CassandraConfig.get_config()
print(cassandra_config.HOST)
cluster = Cluster(
    cassandra_config.HOST,
)

connection = cluster.connect("")
connection.default_timeout = 60


def execute_serially(queries):
    for query in queries:
        connection.execute(query)


city_films_cinema = [
    {
        "city": "Poznań",
        "film": "Matrix",
        "cinema": "Multikino Poznań",
    },
    {
        "city": "Warszawa",
        "film": "Matrix",
        "cinema": "Multikino Warszawa",
    },
    {
        "city": "Warszawa",
        "film": "Pulp Fiction",
        "cinema": "Cinema City Warszawa",
    },
]

cinemas_set = set()
for cfc in city_films_cinema:
    cinemas_set.add(cfc["cinema"])


print("Cassandra connected!")

connection.execute("""
CREATE KEYSPACE IF NOT EXISTS ork_cinema
WITH REPLICATION = { 
'class' : 'SimpleStrategy', 
'replication_factor' :  2
};""")
print("Keyspace created!")

execute_serially(
    [
        "DROP TABLE IF EXISTS ork_cinema.cities",
        "DROP TABLE IF EXISTS ork_cinema.cinemas",
        "DROP TABLE IF EXISTS ork_cinema.films",
        "DROP TABLE IF EXISTS ork_cinema.cinemas_by_film_city",
        "DROP TABLE IF EXISTS ork_cinema.films_by_city",
    ]
)


connection.execute(
    """CREATE TABLE ork_cinema.cities (
  id UUID,
  name TEXT,
  add_info TEXT,
  PRIMARY KEY (id)
);""",
)
connection.execute(
    """INSERT INTO ork_cinema.cities (id, name, add_info) VALUES (uuid(), 'Poznań', 'Wielkopolska');"""
)
connection.execute(
    "INSERT INTO ork_cinema.cities (id, name, add_info) VALUES (uuid(), 'Warszawa', 'Mazowsze');"
)
print("Table ork_cinema.cities created!")

execute_serially(
    [
        """
CREATE TABLE ork_cinema.cinemas (
  id UUID,
  name TEXT,
  PRIMARY KEY (id, name)
);""",
    ]
)
for cinema in cinemas_set:
    connection.execute(
        "INSERT INTO ork_cinema.cinemas (id, name) VALUES (uuid(), %s);", (cinema,)
    )

print("Table ork_cinema.cinemas created!")

execute_serially(
    [
        """CREATE TABLE ork_cinema.films (
  id UUID,
  film_name TEXT,
  PRIMARY KEY (id, film_name)
);""",
        "INSERT INTO ork_cinema.films (id, film_name) VALUES (uuid(), 'Matrix');",
        "INSERT INTO ork_cinema.films (id, film_name) VALUES (uuid(), 'Pulp Fiction');",
    ]
)
print("Table ork_cinema.films created!")

execute_serially(
    [
        """CREATE TABLE ork_cinema.films_by_city (
  city_id UUID,
  film_id UUID,
  film_name TEXT,
  PRIMARY KEY ((city_id), film_id)
);""",
        """CREATE TABLE ork_cinema.cinemas_by_film_city (
  city_id UUID,
  film_id UUID,
  film_name TEXT,
  cinema_id UUID,
  cinema_name TEXT,
  PRIMARY KEY ((film_id, city_id), cinema_id)
);
""",
    ]
)
print("Tables ork_cinema.films_by_city, ork_cinema.cinemas_by_film_city are created!")
time.sleep(3)
city_map = {}
for city in connection.execute("SELECT * FROM ork_cinema.cities"):
    city_map[city.name] = {
        "id": city.id,
        "name": city.name,
    }
print(city_map)

cinemas_map = {}
for cinema in connection.execute("SELECT * FROM ork_cinema.cinemas"):
    cinemas_map[cinema.name] = {
        "id": cinema.id,
        "name": cinema.name,
    }
print(cinemas_map)

films_map = {}
for film in connection.execute("SELECT * FROM ork_cinema.films"):
    films_map[film.film_name] = {
        "id": film.id,
        "film_name": film.film_name,
    }
print(films_map)


# Fill films_by_city
connection.execute(
    "INSERT INTO ork_cinema.films_by_city (city_id, film_id, film_name) VALUES (%s, %s, %s);",
    (city_map["Poznań"]["id"], films_map["Matrix"]["id"], "Matrix"),
)
connection.execute(
    "INSERT INTO ork_cinema.films_by_city (city_id, film_id, film_name) VALUES (%s, %s, %s);",
    (city_map["Warszawa"]["id"], films_map["Matrix"]["id"], "Matrix"),
)
connection.execute(
    "INSERT INTO ork_cinema.films_by_city (city_id, film_id, film_name) VALUES (%s, %s, %s);",
    (city_map["Warszawa"]["id"], films_map["Pulp Fiction"]["id"], "Pulp Fiction"),
)


city_films_cinema = [
    {
        "city": "Poznań",
        "film": "Matrix",
        "cinema": "Multikino Poznań",
    },
    {
        "city": "Warszawa",
        "film": "Matrix",
        "cinema": "Multikino Warszawa",
    },
    {
        "city": "Warszawa",
        "film": "Pulp Fiction",
        "cinema": "Cinema City Warszawa",
    },
]

# Fill cinemas_by_film_city
for cfc in city_films_cinema:
    connection.execute(
        "INSERT INTO ork_cinema.cinemas_by_film_city (city_id, film_id, film_name, cinema_id, cinema_name) VALUES (%s, %s, %s, %s, %s);",
        (
            city_map[cfc["city"]]["id"],
            films_map[cfc["film"]]["id"],
            cfc["film"],
            cinemas_map[cfc["cinema"]]["id"],
            cfc["cinema"],
        ),
    )


execute_serially(
    [
        "DROP TABLE IF EXISTS ork_cinema.timeslots_by_cinema_film",
        """CREATE TABLE ork_cinema.timeslots_by_cinema_film (
  film_id UUID,
  film_name TEXT,
  cinema_id UUID,
  cinema_name TEXT,
  times list<TIMESTAMP>,
  PRIMARY KEY ((film_id, cinema_id))
);""",
    ]
)
print("Table ork_cinema.timeslots_by_cinema_film created!")

timeslots = {
    "2021-10-10 10:00:00": 100,
    "2021-10-10 12:00:00": 20000,
    "2021-10-10 14:00:00": 20000,
    "2021-10-10 16:00:00": 200,
}

for cfc in city_films_cinema:
    connection.execute(
        "INSERT INTO ork_cinema.timeslots_by_cinema_film (film_id, film_name, cinema_id, cinema_name, times) VALUES (%s, %s, %s, %s, %s);",
        (
            films_map[cfc["film"]]["id"],
            cfc["film"],
            cinemas_map[cfc["cinema"]]["id"],
            cfc["cinema"],
            list(timeslots.keys()),
        ),
    )


execute_serially(
    [
        "DROP TABLE IF EXISTS ork_cinema.seats_by_cinema_film_timeslot",
        """CREATE TABLE ork_cinema.seats_by_cinema_film_timeslot (
  cinema_id UUID,
  film_id UUID,
  timeslot TIMESTAMP,
  seat_number INT,
  is_booked BOOLEAN,
  user_name TEXT,
  PRIMARY KEY ((cinema_id, film_id), timeslot, seat_number)
);""",
    ]
)
print("Table ork_cinema.seats_by_cinema_film_timeslot created!")

for timeslot, number_of_seats in timeslots.items():
    for cfc in city_films_cinema:
        for i in range(number_of_seats):
            connection.execute(
                "INSERT INTO ork_cinema.seats_by_cinema_film_timeslot (cinema_id, film_id, timeslot, seat_number, is_booked) VALUES (%s, %s, %s, %s, %s);",
                (
                    cinemas_map[cfc["cinema"]]["id"],
                    films_map[cfc["film"]]["id"],
                    timeslot,
                    i,
                    False,
                ),
            )
execute_serially(
    [
        "DROP TABLE IF EXISTS ork_cinema.booked_seats_by_user",
        """CREATE TABLE ork_cinema.booked_seats_by_user (
  user_name TEXT,
  cinema_id UUID,
  film_id UUID,
  timeslot TIMESTAMP,
  seat_number INT,
  PRIMARY KEY ((user_name), cinema_id, film_id, timeslot, seat_number)
);""",
    ]
)


time.sleep(5)
connection.shutdown()
