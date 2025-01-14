from dotenv import load_dotenv

from .cassandra import CassandraConfig

load_dotenv("./api/.env")

__all__ = ["CassandraConfig"]
