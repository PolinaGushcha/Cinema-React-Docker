from fastapi import Depends, Request
from typing_extensions import Annotated

from .pool import CassandraPool


def get_cassandra_pool(request: Request) -> CassandraPool:
    return request.app.state.cassandra_pool


def get_manager(ManagerClass: type):
    async def get_manager_(
        cassandra_pool: Annotated[CassandraPool, Depends(get_cassandra_pool)],
    ):
        return ManagerClass(cassandra_pool)

    return get_manager_
