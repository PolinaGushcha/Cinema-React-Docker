import asyncio
import datetime
import logging
import uuid

from db.cassandra import CassandraPool

from .seat import BookStatus, Seat, SeatBookStatus
from .times_by_cinema_film import TimesByCinemaFilm

logger = logging.getLogger(__name__)


class SeatInfoManager:
    def __init__(self, cassandra_pool: CassandraPool):
        self.cassandra_pool = cassandra_pool

    async def get_timeslots_by(
        self, cinema_id: uuid.UUID, film_id: uuid.UUID
    ) -> TimesByCinemaFilm:
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(
                session.execute,
                "SELECT * FROM timeslots_by_cinema_film WHERE cinema_id = %s AND film_id = %s",
                (cinema_id, film_id),
            )

            return self._make_times_by_cinema_film(list(result))

    def _make_times_by_cinema_film(self, rows: list[dict]) -> TimesByCinemaFilm:
        if len(rows) == 0:
            return TimesByCinemaFilm(
                cinema_id=uuid.UUID(int=0),
                cinema_name="",
                film_id=uuid.UUID(int=0),
                film_name="",
                times=[],
            )
        row = rows[0]
        return TimesByCinemaFilm(
            cinema_id=row["cinema_id"],
            cinema_name=row["cinema_name"],
            film_id=row["film_id"],
            film_name=row["film_name"],
            times=row["times"],
        )

    async def get_seat_availability(
        self, cinema_id: uuid.UUID, film_id: uuid.UUID, time: datetime.datetime
    ) -> SeatBookStatus:
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(
                session.execute,
                "SELECT seat_number, is_booked FROM seats_by_cinema_film_timeslot WHERE cinema_id = %s AND film_id = %s AND timeslot = %s",
                (cinema_id, film_id, time),
            )
            return self._make_seat_book_status(cinema_id, film_id, time, list(result))

    def _make_seat_book_status(
        self,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        rows: list[dict],
    ) -> SeatBookStatus:
        return SeatBookStatus(
            cinema_id=cinema_id,
            film_id=film_id,
            time=time,
            seats=[
                Seat(
                    seat_number=row["seat_number"],
                    book_status=BookStatus.from_bool(row["is_booked"]),
                )
                for row in rows
            ],
        )

    # async def get_all_films(self):
    #     with await self.cassandra_pool.block() as session:
    #         result = await asyncio.to_thread(session.execute, "SELECT * FROM films")
    #         rows = list(result)
    #         logger.info(rows)
    #         return [Film(**row) for row in rows]

    # async def get_films_by_city(self, city_id: uuid) -> Film:
    #     with await self.cassandra_pool.block() as session:
    #         result = await asyncio.to_thread(
    #             session.execute,
    #             "SELECT * FROM films_by_city WHERE city_id = %s",
    #             (city_id,),
    #         )
    #         return [Film(id=row["film_id"], name=row["film_name"]) for row in result]
