import logging
import uuid

from db.cassandra import get_manager
from db.cities import City, CityManager, get_city_manager
from db.film import CinemasByFilm, Film, FilmManager
from db.timeslots import (
    SeatInfoManager,
    TimesByCinemaFilm,
)
from fastapi import APIRouter, Depends
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

router = APIRouter(tags=["cinemas"], prefix="/cinemas")


@router.get("/get_cities", summary="Get all cities where we have attached cinemas.")
async def get_cities(
    city_manager: Annotated[CityManager, Depends(get_city_manager)],
) -> list[City]:
    cities = await city_manager.get_all_cities()
    return cities


@router.get(
    "/get_films_by_city", summary="Get all films that are available in the city."
)
async def get_films_by_city(
    city_id: uuid.UUID,
    film_manager: Annotated[FilmManager, Depends(get_manager(FilmManager))],
) -> list[Film]:
    return await film_manager.get_films_by(city_id)


@router.get(
    "/get_cinemas_by_film", summary="Get all cinemas where the film is available."
)
async def get_cinemas_by_film(
    city_id: uuid.UUID,
    film_id: uuid.UUID,
    film_manager: Annotated[FilmManager, Depends(get_manager(FilmManager))],
) -> CinemasByFilm:
    return await film_manager.get_cinemas_by_film(city_id, film_id)


@router.get("/get_timeslots", summary="Get all timeslots for the cinema and film.")
async def get_timeslots(
    cinema_id: uuid.UUID,
    film_id: uuid.UUID,
    book_manager: Annotated[SeatInfoManager, Depends(get_manager(SeatInfoManager))],
) -> TimesByCinemaFilm:
    return await book_manager.get_timeslots_by(cinema_id, film_id)
