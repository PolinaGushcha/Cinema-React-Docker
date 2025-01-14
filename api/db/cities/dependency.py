from fastapi import Depends
from typing_extensions import Annotated

from db.cassandra import CassandraPool, get_cassandra_pool

from .city_manager import CityManager


async def get_city_manager(
    cassandra_pool: Annotated[CassandraPool, Depends(get_cassandra_pool)],
) -> CityManager:
    return CityManager(cassandra_pool)
