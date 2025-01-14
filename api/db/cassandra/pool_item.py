from cassandra.cluster import Session
from cassandra.query import dict_factory


class CassandraPoolItem:
    def __init__(self, session: Session, index: int) -> None:
        session.row_factory = dict_factory
        self.session = session
        self.is_free = True
        self.index = index

    def block(self):
        if self.is_free is False:
            raise ValueError("This item is alread blocked")
        self.is_free = False

    def release(self):
        if self.is_free is True:
            raise ValueError("This item is alread free")
        self.is_free = True

    def __enter__(self):
        self.is_free = False
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.is_free = True
