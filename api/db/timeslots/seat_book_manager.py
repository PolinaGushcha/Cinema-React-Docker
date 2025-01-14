import asyncio
import datetime
import logging
import uuid

from cassandra.query import BatchStatement

from db.cassandra import CassandraPool

from .exceptions import SeatAreAlreadyBookedException, SomeSeatAreAlreadyFreeException
from .seat import BookStatus

logger = logging.getLogger(__name__)


class SeatBookManager:
    def __init__(self, cassandra_pool: CassandraPool):
        self.cassandra_pool = cassandra_pool

    async def book_seat(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        await self._update_timeslots(
            user_name, cinema_id, film_id, time, seat_numbers, BookStatus.BOOKED
        )
        await self._store_booked_seat_information(
            user_name, cinema_id, film_id, time, seat_numbers
        )

    async def unbook_seat(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        await self._update_timeslots(
            user_name, cinema_id, film_id, time, seat_numbers, BookStatus.AVAILABLE
        )
        await self._remove_booked_seat_information(
            user_name, cinema_id, film_id, time, seat_numbers
        )

    async def change_time(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        old_time: datetime.datetime,
        new_time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        await self._update_time(
            user_name, cinema_id, film_id, old_time, new_time, seat_numbers
        )
        await self._remove_booked_seat_information(
            user_name, cinema_id, film_id, old_time, seat_numbers
        )
        await self._store_booked_seat_information(
            user_name, cinema_id, film_id, new_time, seat_numbers
        )

    async def _update_timeslots(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        seat_numbers: list[int],
        book_status: BookStatus,
    ) -> None:
        with await self.cassandra_pool.block() as session:
            batch = BatchStatement()
            for seat_number in seat_numbers:
                batch.add(
                    session.prepare(
                        "UPDATE seats_by_cinema_film_timeslot SET is_booked = ?, user_name = ? WHERE cinema_id = ? AND film_id = ? AND timeslot = ? AND seat_number = ? IF is_booked = ? AND user_name = ?;"
                    ),
                    (
                        book_status.is_booked,
                        user_name if book_status == BookStatus.BOOKED else None,
                        cinema_id,
                        film_id,
                        time,
                        seat_number,
                        not book_status.is_booked,
                        None if book_status == BookStatus.BOOKED else user_name,
                    ),
                )
            res = await asyncio.to_thread(
                session.execute,
                batch,
            )
            if res.was_applied:
                return

            if book_status == BookStatus.BOOKED:
                raise SeatAreAlreadyBookedException("Seat already booked")
            if book_status == BookStatus.AVAILABLE:
                raise SomeSeatAreAlreadyFreeException("Some seat is already free")

    async def _store_booked_seat_information(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        with await self.cassandra_pool.block() as session:
            batch = BatchStatement()
            for seat_number in seat_numbers:
                batch.add(
                    session.prepare(
                        "INSERT INTO booked_seats_by_user (user_name, cinema_id, film_id, timeslot, seat_number) VALUES (?, ?, ?, ?, ?);"
                    ),
                    (user_name, cinema_id, film_id, time, seat_number),
                )
            await asyncio.to_thread(
                session.execute,
                batch,
            )

    async def _remove_booked_seat_information(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        with await self.cassandra_pool.block() as session:
            batch = BatchStatement()
            for seat_number in seat_numbers:
                batch.add(
                    session.prepare(
                        "DELETE FROM booked_seats_by_user WHERE user_name = ? AND cinema_id = ? AND film_id = ? AND timeslot = ? AND seat_number = ?;"
                    ),
                    (user_name, cinema_id, film_id, time, seat_number),
                )
            await asyncio.to_thread(
                session.execute,
                batch,
            )

    async def _update_time(
        self,
        user_name: str,
        cinema_id: uuid.UUID,
        film_id: uuid.UUID,
        old_time: datetime.datetime,
        new_time: datetime.datetime,
        seat_numbers: list[int],
    ) -> None:
        with await self.cassandra_pool.block() as session:
            batch = BatchStatement()
            book_new_prep = session.prepare(
                """
                UPDATE seats_by_cinema_film_timeslot 
                SET is_booked = ?, user_name = ? 
                WHERE cinema_id = ? AND film_id = ? AND timeslot = ? AND seat_number = ? 
                IF is_booked = ? AND user_name = ?;
                """
            )
            for seat_number in seat_numbers:
                logger.info(
                    f"Updating seat {seat_number} from {old_time} to {new_time}"
                )
                batch.add(
                    book_new_prep,
                    (
                        True,  # SET: is_booked
                        user_name,  # SET: user_name
                        cinema_id,  # WHERE: cinema_id
                        film_id,  # WHERE: film_id
                        new_time,  # WHERE: timeslot
                        seat_number,  # WHERE: seat_number
                        False,  # IF: is_booked
                        None,  # IF: user_name
                    ),
                )
                batch.add(
                    book_new_prep,
                    (
                        False,
                        None,
                        cinema_id,
                        film_id,
                        old_time,
                        seat_number,
                        True,
                        user_name,
                    ),
                )

            res = await asyncio.to_thread(
                session.execute,
                batch,
            )
            if res.was_applied:
                return
            raise SeatAreAlreadyBookedException("Seat already booked")
