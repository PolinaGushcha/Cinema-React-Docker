import logging

from db.cassandra import get_manager
from db.user import UserBooks, UserBooksManager
from fastapi import APIRouter, Depends
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/get_booked_seats", summary="Gets booked seats for a user(by his name).")
async def get_booked_seats(
    user_name: str,
    user_manager: Annotated[UserBooksManager, Depends(get_manager(UserBooksManager))],
) -> UserBooks:
    return await user_manager.get_booked_slots(user_name)
