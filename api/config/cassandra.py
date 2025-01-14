import logging
import os
from functools import cache

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CassandraConfig(BaseModel):
    HOST: list[tuple[str, int]]

    @cache
    @staticmethod
    def get_config():
        logger.info("Getting Cassandra config...")
        logger.info(f"Using cassandra host: {os.environ.get('CASSANDRA_HOST')}")
        return CassandraConfig(
            HOST=[
                CassandraConfig._parse_host(host)
                for host in os.environ.get("CASSANDRA_HOST").split(",")
            ]
        )

    @staticmethod
    def _parse_host(host: str) -> tuple[str, int]:
        host, port = host.split(":")
        return host, int(port)
