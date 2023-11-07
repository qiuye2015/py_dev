#!/usr/bin/env python3
import os

import sqlalchemy

from tools.tool_orm.sqlalchemy_demo.base_driver import BaseDriver

# from webapps.common.database.base_driver import BaseDriver

MYSQL_URI_PATTERN = 'mysql+{connector}://{username}:{password}@{hostname}:{port}/{database}'
# TODO(yuan.ye): make driver charset for configurable
# MYSQL_URI_WITH_CHARSET_PATTERN = '{mysql_uri}?charset={charset}&collation=utf8mb4_general_ci'
MYSQL_URI_WITH_CHARSET_PATTERN = '{mysql_uri}?charset={charset}'

# https://docs.sqlalchemy.org/en/13/core/pooling.html
# pessimistic or optimistic
SQLALCHEMY_DISCONNECT_HANDLING = os.getenv('SQLALCHEMY_DISCONNECT_HANDLING', 'optimistic')
SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '60'))
SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', '50'))
SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '20'))


def get_engine_configs():
    if SQLALCHEMY_DISCONNECT_HANDLING == 'optimistic':
        return {
            'pool_recycle': SQLALCHEMY_POOL_RECYCLE,
            'pool_size': SQLALCHEMY_POOL_SIZE,
            'max_overflow': SQLALCHEMY_MAX_OVERFLOW,
        }
    return {
        'pool_pre_ping': True,
        'pool_size': SQLALCHEMY_POOL_SIZE,
        'max_overflow': SQLALCHEMY_MAX_OVERFLOW,
    }


class MySQLDriver(BaseDriver):
    """MySQL driver"""

    @classmethod
    def create_engine(cls, config=None):
        if not config:
            raise ValueError('No config provided!')
        mysql_uri = (
            config.MYSQL_URI
            if config.MYSQL_URI
            else MYSQL_URI_PATTERN.format(
                connector=config.MYSQL_CONNECTOR,
                username=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                hostname=config.MYSQL_HOST,
                database=config.MYSQL_DATABASE,
                port=config.MYSQL_PORT,
            )
        )
        return sqlalchemy.create_engine(
            MYSQL_URI_WITH_CHARSET_PATTERN.format(mysql_uri=mysql_uri, charset='utf8mb4'),
            convert_unicode=False,
            encoding='utf8',
            # echo=True, # 测试SQL时打开注释
            **get_engine_configs(),
        )

    @classmethod
    def create_extra_engines(cls, extra_configs):
        return {key: cls.create_engine(config) for key, config in extra_configs.items()}
