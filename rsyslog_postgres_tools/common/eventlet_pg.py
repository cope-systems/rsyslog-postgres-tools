from functools import wraps
from contextlib import contextmanager
from psycogreen.eventlet import patch_psycopg
import psycopg2
from collections import OrderedDict
from eventlet.db_pool import RawConnectionPool
from psycopg2.extras import DictRow, DictCursorBase


class DictRowHack(DictRow):
    """
    DictRowHack class

    """
    def __getitem__(self, item):
        if isinstance(item, str):
            return super(DictRowHack, self).__getitem__(item.lower())

        return super(DictRowHack, self).__getitem__(item)

    def get(self, item, default=None):
        """
        Get
        :param item:
        :param default:
        :return:
        """
        if isinstance(item, str):
            return super(DictRowHack, self).get(item.lower(), default)
        else:
            return super(DictRowHack, self).get(item, default)


class DictCursorHack(DictCursorBase):
    """A cursor that provides some what case-insensitive results."""

    def __init__(self, *args, **kwargs):
        kwargs['row_factory'] = DictRowHack
        super(DictCursorHack, self).__init__(*args, **kwargs)
        self._prefetch = 1

    def execute(self, query, variables=None):
        """
        Execute

        :param query:
        :param variables:
        :return:
        """
        self.index = OrderedDict()
        self._query_executed = 1
        return super(DictCursorHack, self).execute(query, variables)

    def callproc(self, procname, variables=None):
        """
        Callproc

        :param procname:
        :param variables:
        :return:
        """
        self.index = OrderedDict()
        self._query_executed = 1
        return super(DictCursorHack, self).callproc(procname, variables)

    def _build_index(self):
        """
        Build index

        :return:
        """
        if self._query_executed == 1 and self.description:
            for i in range(len(self.description)):
                self.index[self.description[i][0]] = i
            self._query_executed = 0


@wraps(psycopg2.connect)
def regular_connect(*args, **kwargs):
    kwargs.update(cursor_factory=DictCursorHack)
    connection = psycopg2.connect(*args, **kwargs)
    return connection


class GreenPsycopg2(object):
    @staticmethod
    @wraps(psycopg2.connect)
    def connect(*args, **kwargs):
        patch_psycopg()
        kwargs.update(cursor_factory=DictCursorHack)
        connection = psycopg2.connect(*args, **kwargs)
        return connection


def create_green_psycopg_pool(connection_url, min_size=2, max_size=20, max_idle=10, max_age=30,
                              connect_timeout=5):
    return RawConnectionPool(
        GreenPsycopg2,
        min_size=min_size,
        max_size=max_size,
        max_idle=max_idle,
        max_age=max_age,
        connect_timeout=connect_timeout,
        dsn=connection_url
    )


@contextmanager
def get_pool_connection(pool):
    conn = None
    try:
        conn = pool.get()
        yield conn
    finally:
        if conn is not None:
            pool.put(conn)
