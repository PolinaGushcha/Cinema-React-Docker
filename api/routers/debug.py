from db.cassandra import get_manager
from db.film import Film, FilmManager
from fastapi import APIRouter, Depends
from typing_extensions import Annotated

router = APIRouter(tags=["debug"])


@router.get("/debug_get_films")
async def debug_get_films(
    film_manager: Annotated[FilmManager, Depends(get_manager(FilmManager))],
) -> list[Film]:
    return await film_manager.get_all_films()
