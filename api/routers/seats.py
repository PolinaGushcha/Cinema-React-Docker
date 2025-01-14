import datetime
import logging
import uuid

from db.cassandra import get_manager
from db.timeslots import (
    SeatAreAlreadyBookedException,
    SeatBookManager,
    SeatBookStatus,
    SeatInfoManager,
    SomeSeatAreAlreadyFreeException,
)
from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from update_status import UpdateStatus

logger = logging.getLogger(__name__)

router = APIRouter(tags=["seats"], prefix="/seats")


@router.get("/get_seats", summary="Get seats availability for a cinema, film and time.")
async def get_seats(
    cinema_id: uuid.UUID,
    film_id: uuid.UUID,
    time: datetime.datetime,
    book_manager: Annotated[SeatInfoManager, Depends(get_manager(SeatInfoManager))],
) -> SeatBookStatus:
    return await book_manager.get_seat_availability(cinema_id, film_id, time)


@router.post(
    "/book",
    summary="Book seats for a user.",
    description="If some seats are already booked or not exists in the table, "
    + f"the whole operation will be canceled. It returns '{UpdateStatus.SUCCESS.value}' if all seats are booked successfully, "
    + f"otherwise '{UpdateStatus.FAIL.value}'.",
)
async def book_seat(
    user_name: str,
    cinema_id: uuid.UUID,
    film_id: uuid.UUID,
    time: datetime.datetime,
    seat_numbers: list[int],
    book_manager: Annotated[SeatBookManager, Depends(get_manager(SeatBookManager))],
) -> UpdateStatus:
    try:
        await book_manager.book_seat(user_name, cinema_id, film_id, time, seat_numbers)
        return UpdateStatus.SUCCESS
    except SeatAreAlreadyBookedException:
        return UpdateStatus.FAIL


@router.post(
    "/unbook",
    summary="Cancel the book for seats for a user.",
    description="If some seats are already free or not exists in the table "
    + "or seats are booked by another user, the whole operation will be canceled. "
    + f"The operation returns '{UpdateStatus.SUCCESS.value}' if all seats are unbooked successfully, "
    + f"otherwise '{UpdateStatus.FAIL.value}'.",
)
async def unbook_seat(
    user_name: str,
    cinema_id: uuid.UUID,
    film_id: uuid.UUID,
    time: datetime.datetime,
    seat_numbers: list[int],
    book_manager: Annotated[SeatBookManager, Depends(get_manager(SeatBookManager))],
) -> UpdateStatus:
    try:
        await book_manager.unbook_seat(
            user_name, cinema_id, film_id, time, seat_numbers
        )
        return UpdateStatus.SUCCESS
    except SomeSeatAreAlreadyFreeException:
        return UpdateStatus.FAIL


@router.post(
    "/change_time",
    summary="Change the time for the booked seats.",
    description="It changes seats in the score of cinema and film(they must be the same)"
    + "from the old time to the new time. If some seats are already booked or not exists in the table"
    + "or some seats are already free or booked by another user, the whole operation will be canceled."
    + f"The operation returns '{UpdateStatus.SUCCESS.value}' if all seats are unbooked successfully, "
    + f"otherwise '{UpdateStatus.FAIL.value}'.",
)
async def change_time(
    user_name: str,
    cinema_id: uuid.UUID,
    film_id: uuid.UUID,
    old_time: datetime.datetime,
    new_time: datetime.datetime,
    seat_numbers: list[int],
    book_manager: Annotated[SeatBookManager, Depends(get_manager(SeatBookManager))],
) -> UpdateStatus:
    try:
        await book_manager.change_time(
            user_name, cinema_id, film_id, old_time, new_time, seat_numbers
        )
        return UpdateStatus.SUCCESS
    except SeatAreAlreadyBookedException:
        return UpdateStatus.FAIL
