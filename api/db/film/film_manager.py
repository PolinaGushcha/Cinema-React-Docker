import asyncio
import logging
import uuid

from db.cassandra import CassandraPool

from .cinema import Cinema
from .cinemas_by_film import CinemasByFilm
from .film import Film

logger = logging.getLogger(__name__)


class FilmManager:
    def __init__(self, cassandra_pool: CassandraPool):
        self.cassandra_pool = cassandra_pool

    async def get_films_by(self, city_id: uuid.UUID) -> list[Film]:
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(
                session.execute,
                "SELECT * FROM films_by_city WHERE city_id = %s",
                (city_id,),
            )
            return [Film(id=row["film_id"], name=row["film_name"]) for row in result]

    async def get_cinemas_by_film(
        self, city_id: uuid.UUID, film_id: uuid.UUID
    ) -> CinemasByFilm:
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(
                session.execute,
                "SELECT * FROM cinemas_by_film_city WHERE city_id = %s and film_id = %s",
                (city_id, film_id),
            )
            return self._make_cinemas_by_film(list(result))

    def _make_cinemas_by_film(self, rows: list[dict]) -> CinemasByFilm:
        city_id: uuid.UUID = None
        film: Film = None
        cinemas: list[Cinema] = []
        for row in rows:
            if film is None:
                film = Film(id=row["film_id"], name=row["film_name"])
                city_id = row["city_id"]
            cinemas.append(Cinema(id=row["cinema_id"], name=row["cinema_name"]))
        return CinemasByFilm(city_id=city_id, film=film, cinemas=cinemas)
