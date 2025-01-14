import asyncio
import datetime
import logging
import uuid

from pydantic import BaseModel

from db.cassandra import CassandraPool

from .user_books import UserBookFilm, UserBooks

logger = logging.getLogger(__name__)


class CinemaFilmCombination:
    def __init__(self, cinema_id: uuid.UUID, film_id: uuid.UUID):
        self.cinema_id = cinema_id
        self.film_id = film_id

    def __str__(self):
        return f"{self.cinema_id},{self.film_id})"

    def __hash__(self) -> int:
        return hash((self.cinema_id, self.film_id))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CinemaFilmCombination):
            return False
        return self.cinema_id == other.cinema_id and self.film_id == other.film_id

    def __ne__(self, other: object) -> bool:
        return not self == other


class CinemaFilmTimeCombination:
    def __init__(
        self, cinema_id: uuid.UUID, film_id: uuid.UUID, time: datetime.datetime
    ):
        self.cinema_id = cinema_id
        self.film_id = film_id
        self.time = time

    @property
    def cinema_film_combination(self) -> CinemaFilmCombination:
        return CinemaFilmCombination(self.cinema_id, self.film_id)

    def __str__(self):
        return f"{self.cinema_id},{self.film_id}),{self.time})"

    def __hash__(self) -> int:
        return hash((self.cinema_id, self.film_id, self.time))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CinemaFilmTimeCombination):
            return False
        return (
            self.cinema_id == other.cinema_id
            and self.film_id == other.film_id
            and self.time == other.time
        )

    def __ne__(self, other: object) -> bool:
        return not self == other


class CinemaFilm(BaseModel):
    cinema_id: uuid.UUID
    cinema_name: str
    film_id: uuid.UUID
    film_name: str


class UserBooksManager:
    def __init__(self, cassandra_pool: CassandraPool):
        self.cassandra_pool = cassandra_pool

    async def get_booked_slots(self, user_name: str) -> UserBooks:
        raw_data = await self._get_times_with_ids(user_name)
        combinations = self._filter_unique_cinema_film_times(raw_data)
        cinema_map = await self._fetch_cinema_film_time(combinations)
        return self._map_raw_data(user_name, raw_data, cinema_map)

    async def _get_times_with_ids(self, user_name: str) -> list[dict]:
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(
                session.execute,
                "SELECT * FROM booked_seats_by_user WHERE user_name = %s",
                (user_name,),
            )
            return list(result)

    def _filter_unique_cinema_film_times(
        self, raw_data: list[dict]
    ) -> set[CinemaFilmCombination]:
        combinations = set()
        for row in raw_data:
            combination = CinemaFilmCombination(row["cinema_id"], row["film_id"])
            combinations.add(combination)
        return combinations

    async def _fetch_cinema_film_time(
        self, combinations: set[CinemaFilmCombination]
    ) -> dict[CinemaFilmCombination, CinemaFilm]:
        cinema_map = {}
        with await self.cassandra_pool.block() as session:
            prepared = session.prepare(
                "SELECT film_id, film_name, cinema_id, cinema_name FROM timeslots_by_cinema_film WHERE cinema_id = ? AND film_id = ?"
            )
            for combination in combinations:
                result = await asyncio.to_thread(
                    session.execute,
                    prepared,
                    (combination.cinema_id, combination.film_id),
                )
                row = list(result)[0]
                cinema_map[combination] = CinemaFilm(
                    cinema_id=row["cinema_id"],
                    cinema_name=row["cinema_name"],
                    film_id=row["film_id"],
                    film_name=row["film_name"],
                )
        return cinema_map

    def _map_raw_data(
        self,
        user_name: str,
        raw_data: list[dict],
        map_table: dict[CinemaFilmCombination, CinemaFilm],
    ) -> UserBooks:
        time_slots = {}
        for row in raw_data:
            combination = CinemaFilmTimeCombination(
                row["cinema_id"], row["film_id"], row["timeslot"]
            )
            if combination not in time_slots:
                map_row = map_table[combination.cinema_film_combination]
                time_slots[combination] = UserBookFilm(
                    cinema_id=map_row.cinema_id,
                    cinema_name=map_row.cinema_name,
                    film_id=map_row.film_id,
                    film_name=map_row.film_name,
                    time=combination.time,
                    seats=[row["seat_number"]],
                )
            else:
                time_slots[combination].seats.append(row["seat_number"])
        return UserBooks(user_name=user_name, books=list(time_slots.values()))
