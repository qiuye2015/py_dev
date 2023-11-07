import atexit
import logging
import os
import threading

from playhouse.pool import PooledMySQLDatabase

from config import Config

_db = PooledMySQLDatabase(None)


# 对外
def get_db():
    # 以下划线'_'开头的变量为私有变量
    return _db


def _init_db():
    _db.init(
        Config.get("MYSQL_DATABASE"),
        timeout=3,
        stale_timeout=1800,
        max_connections=10,
        user=Config.get("MYSQL_USER"),
        password=Config.get("MYSQL_PASS"),
        host=Config.get("MYSQL_HOST"),
        port=int(Config.get("MYSQL_PORT")),
        charset='utf8mb4',
    )
    logging.info("db inited")
    return _db


class DbClient(object):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    logging.info('db client init:{}'.format(os.getpid()))
                    cls._instance = _init_db()

        return cls._instance


# 对外
def new_mysql_client():
    return DbClient()


class ConnectionContext(object):
    def __init__(self, _db):
        self.db = _db
        self.is_connect_entry = False

    def __enter__(self):
        if self.db.is_closed():
            logging.info("db is closed, connect...")
            self.db.connect()
            self.is_connect_entry = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_connect_entry:
            logging.info("db close because connect retried")
            self.db.close()


# 对外
def connection_context(_db):
    return ConnectionContext(_db)


@atexit.register
def close():
    try:
        if not _db.deferred:
            _db.close_all()
        logging.info('db closed!!!, %s', os.getpid())
    except BaseException as e:
        logging.error(e)
