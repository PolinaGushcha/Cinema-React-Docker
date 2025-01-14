import asyncio

from cassandra.cluster import Cluster

from .pool_item import CassandraPoolItem


class CassandraPool:
    def __init__(
        self,
        cluster: Cluster,
        amount: int,
        registration_map: dict[str, type] | None = None,
    ) -> None:
        registration_map = registration_map if registration_map is not None else {}
        self._sem = asyncio.Semaphore(1)

        for table, klass in registration_map.items():
            cluster.register_user_type("ork_cinema", table, klass)

        self._items = [
            CassandraPoolItem(cluster.connect("ork_cinema"), i) for i in range(amount)
        ]

    async def block(self) -> CassandraPoolItem:
        async with self._sem:
            while True:
                free_item = self._get_free()
                if free_item is not None:
                    free_item.block()
                    return free_item
                await asyncio.sleep(0)

    def release(self, free_item: CassandraPoolItem) -> None:
        free_item.release()

    def _get_free(self) -> CassandraPoolItem | None:
        for item in self._items:
            if item.is_free:
                return item
        return None
