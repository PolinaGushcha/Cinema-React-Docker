import asyncio
import logging

from db.cassandra import CassandraPool

from .city import City

logger = logging.getLogger(__name__)


class CityManager:
    def __init__(self, cassandra_pool: CassandraPool):
        self.cassandra_pool = cassandra_pool

    async def get_all_cities(self):
        with await self.cassandra_pool.block() as session:
            result = await asyncio.to_thread(session.execute, "SELECT * FROM cities")
            rows = list(result)
            logger.info(rows)
            return [City(**row) for row in rows]
