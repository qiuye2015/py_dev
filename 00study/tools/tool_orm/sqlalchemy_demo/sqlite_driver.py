#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy.pool import StaticPool

from tools.tool_orm.sqlalchemy_demo.base_driver import BaseDriver


# from webapps.common.database.base_driver import BaseDriver


class SQLiteDriver(BaseDriver):
    """SQLite driver"""

    @classmethod
    def create_engine(cls, config=None):
        """
        Since SQLite uses SingletonThreadPool or NullPool,
        max_overflow is not supported.
        :return: database engine
        """
        return sqlalchemy.create_engine(
            "sqlite://",
            convert_unicode=False,
            poolclass=StaticPool,
            connect_args={
                'check_same_thread': False,
            },
        )

    @classmethod
    def map_column_type(cls, column):
        if type(column.type) in [sqlalchemy.BigInteger, sqlalchemy.BIGINT]:
            column.type = sqlalchemy.Integer()
        elif type(column.type) == sqlalchemy.DECIMAL:
            column.type = sqlalchemy.FLOAT()
        elif type(column.type) in [sqlalchemy.TEXT, sqlalchemy.Text]:
            # Remove collation, if any
            column.type = sqlalchemy.TEXT()
        elif type(column.type) in [sqlalchemy.VARCHAR, sqlalchemy.String]:
            # Remove collation, if any
            column.type = sqlalchemy.VARCHAR()
