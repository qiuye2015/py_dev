#!/usr/bin/env python3
# pylint: disable=protected-access
from collections import OrderedDict
from collections.abc import Iterable
import inspect
from itertools import islice
import logging
import os
from time import sleep
import typing

from sqlalchemy import desc, func, inspect as alchemy_inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import joinedload, scoped_session, sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import operators

from tools.tool_orm.sqlalchemy_demo.model_base import DeclarativeBase
from tools.tool_orm.sqlalchemy_demo.mysql_driver import MySQLDriver
from tools.tool_orm.sqlalchemy_demo.sqlite_driver import SQLiteDriver

# from webapps.common.database.model_base import DeclarativeBase
# from webapps.common.database.mysql_driver import MySQLDriver
# from webapps.common.database.sqlite_driver import SQLiteDriver

# 0 means no retry.
SQLALCHEMY_MAX_RETRY = int(os.getenv('SQLALCHEMY_MAX_RETRY', '0'))


def is_retriable_exceptions(ex):
    error_messages = [
        'Lost connection to MySQL server during query',
    ]
    for msg in error_messages:
        if msg in str(ex):
            return True
    return False


def get_tables_for_bind(bind):
    """
    Returns a list of all tables relevant for a bind.
    bind might be `None`
    """
    result = []
    for model_class in DeclarativeBase.registry._class_registry.values():
        if not hasattr(model_class, '__table__') or not any(
            map(lambda cls: cls.__name__ == 'ModelBase', inspect.getmro(model_class))
        ):
            continue
        if getattr(model_class, 'BIND_KEY', None) == bind:
            result.append(model_class.__table__)
    return result


# pylint: disable=too-many-ancestors
class RetryingQuery(Query):
    _max_retry = SQLALCHEMY_MAX_RETRY

    def __iter__(self):
        attempts = 1
        while attempts <= self._max_retry:
            try:
                return super().__iter__()
            except OperationalError as ex:
                if not is_retriable_exceptions(ex):
                    raise
                sleep_for = 0.01 * 2 ** (attempts - 1)
                logging.error(
                    'Database connection error: retrying => sleep for {}s'
                    'and will retry (attempts #{} of {}) \n Impacted query: {}'.format(
                        sleep_for, attempts, self._max_retry, ex
                    )
                )
                sleep(sleep_for)
                attempts += 1


class Database:
    """
    The global interface to access databases.
    """

    instance = None
    initialized = False

    @classmethod
    def get_instance(cls) -> 'Database':
        """Return the globally unique instance of Database"""
        if not cls.initialized or not cls.instance:
            cls.init()
        return cls.instance

    @classmethod
    def init(cls, driver_class=None, **options):
        """
        Database.init function should be the first call of an application to initialize Database
        configs.

        The Database class provides multiple implementations (e.g. MySQL & SQLite). The config file
        should decide which implementation to use while Application layer should always call
        Database.init() instead of MySQLDatabase.init() or SQLiteDatabase.init().
        """
        config = options.get('config')
        # Set local config to sqlite in order to run Unit test.
        if config and config.DATABASE_DRIVER == 'sqlite':
            driver_class = SQLiteDriver
        if not driver_class:
            driver_class = MySQLDriver
        cls.initialized = True
        cls.driver_class = driver_class
        if not cls.instance:
            cls.instance = cls(**options)

    def __init__(self, **options):
        """
        Create a Database instance with a given driver.
        """
        self.engine = self.driver_class.create_engine(options.get('config'))
        kwargs = {
            'expire_on_commit': False,
            'autoflush': False,
            'autocommit': False,
        }
        if 'binds' in options:
            binds = {}
            self.extra_engines = self.driver_class.create_extra_engines(options['binds'])
            binds_list = [None] + list(options['binds'].keys())
            for bind_key in binds_list:
                engine = self.extra_engines.get(bind_key, self.engine)
                tables = get_tables_for_bind(bind_key)
                binds.update(dict((table, engine) for table in tables))
            self.extra_session_factories = {
                key: scoped_session(
                    sessionmaker(bind=engine, **kwargs),
                )
                for key, engine in self.extra_engines.items()
            }
            kwargs['binds'] = binds
        kwargs['bind'] = self.engine
        if SQLALCHEMY_MAX_RETRY:
            self.session_factory = scoped_session(
                sessionmaker(query_cls=RetryingQuery, **kwargs),
            )
        else:
            self.session_factory = scoped_session(
                sessionmaker(**kwargs),
            )

    @classmethod
    def get_session(cls) -> scoped_session:
        """
        Return a SQLAlchemy session.

        Don't use this function directly unless you know what you are doing.
        """
        return cls.get_instance().session_factory()

    @classmethod
    def get_one(cls, model_type, model_id: int or str, for_update=False):
        """
        Retrieve model by type and id.
        """
        if not isinstance(model_id, int):
            try:
                model_id = int(model_id)
            except (TypeError, ValueError) as e:
                if isinstance(model_id, operators.Operators):
                    raise TypeError('Invalid model_id - you probably meant to ' 'use Database.get_one_by') from e
                return None
        if not model_id or model_id <= 0:
            # fail fast if model_id is not a valid database id
            return None
        query = cls.get_session().query(model_type)
        if for_update:
            query = query.with_for_update()
        return query.get(model_id)

    @classmethod
    def get_many(cls, model_type, model_ids: typing.List) -> OrderedDict:
        """
        Retrieve models by type and ids.
        """
        if not model_ids:
            return OrderedDict()
        models = cls.get_session().query(model_type).filter(model_type.id.in_(model_ids)).all()
        models_dict = {model.id: model for model in models}
        return OrderedDict([(model_id, models_dict.get(model_id)) for model_id in model_ids])

    @classmethod
    def get_all(cls, model_type):
        """
        Helpful function to retrieve all models of a given type.

        Don't call unless you know what you are doing.
        """
        return cls.get_session().query(model_type).all()

    @classmethod
    def get_one_by(cls, model_type, *filters, order_by=None, for_update=False):
        """
        Retrieve model by type、 filters and order_by.
        """
        query = cls.get_session().query(model_type).filter(*filters)
        if order_by is not None:
            if isinstance(order_by, str) and order_by and order_by[0] == '-':
                order_by = desc(order_by[1:])
            query = query.order_by(order_by)
        if for_update:
            query = query.with_for_update()
        return query.first()

    @classmethod
    def get_many_by(cls, model_type, *filters, order_by=None, offset=None, limit=None) -> OrderedDict:
        """
        Retrieve models by type and filters. Results returned as an ordered dict.
        """
        models = cls.get_many_as_list_by(model_type, *filters, order_by=order_by, offset=offset, limit=limit)
        return OrderedDict([(model.id, model) for model in models])

    @classmethod
    def get_many_as_list_by(
        cls, model_type, *filters, order_by=None, offset=None, limit=None, joinedloads=None, for_update=False
    ) -> typing.List:
        """Retrieve models by type and filters. Results returned as a list.
        :joinedloads: the relationship fields of the model_type, used to eager load the field
                      by joining with the field type when run the SELECT sql operation.
                      It's recommended that if you have to get these relationship fields
                      of the returning list
        :order_by: it could be a ColumnElement object, such as:
                       Table.column, Table.column.desc(), desc(Table.column)
                   or it could be string literal which would be coerced into a ColumnElement, e.g.:
                       "column", "-column", "column desc",
                   or it could be full sql expression in string, e.g.:
                       text("some special expression")
                   reference:
                   https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.order_by
                   https://docs.sqlalchemy.org/en/13/core/sqlelement.html#column-elements-and-expressions
                   https://docs.sqlalchemy.org/en/13/changelog/migration_10.html#order-by-and-group-by-are-special-cases
        """
        query = cls.extend_query_by(
            cls.get_session().query(model_type),
            *filters,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )
        if joinedloads:
            query = query.options(*[joinedload(f) for f in joinedloads])
        if for_update:
            query = query.with_for_update()
        return query.all()

    @classmethod
    def get_count_by(cls, model_type, *filters):
        model_inspect = alchemy_inspect(model_type)
        primary_key = model_inspect.primary_key[0]
        return cls.get_session().query(func.count(primary_key)).filter(*filters).scalar()

    @classmethod
    def delete(cls, object_or_objects):
        if not isinstance(object_or_objects, Iterable):
            object_or_objects = [object_or_objects]

        session = cls.get_session()
        for obj in object_or_objects:
            session.delete(obj)

    @classmethod
    def delete_by(cls, model_type, *filters):
        cls.get_session().query(model_type).filter(*filters).delete(synchronize_session=False)

    @classmethod
    def add(cls, object_or_objects, need_commit=False):
        if isinstance(object_or_objects, Iterable):
            cls.get_session().add_all(object_or_objects)
        else:
            cls.get_session().add(object_or_objects)
        if need_commit:
            cls.get_session().commit()

    @classmethod
    def batch_add_commit(cls, objects, batch_size=10000):
        if not objects:
            return
        objects = (obj for obj in objects if not obj.id)
        while True:
            batch_objects = list(islice(objects, batch_size))
            if not batch_objects:
                return
            Database.add(batch_objects)
            Database.commit()

    @classmethod
    def bulk_add_commit(cls, objects, batch_size=1000):
        objects = (obj for obj in objects if not obj.id)
        while True:
            batch_objects = list(islice(objects, batch_size))
            if not batch_objects:
                return
            Database.get_session().bulk_save_objects(batch_objects)
            Database.commit()

    @classmethod
    def bulk_update_commit(cls, model_type, update_dicts, need_commit=True):
        cls.get_session().bulk_update_mappings(model_type, update_dicts)
        if need_commit:
            Database.commit()

    @classmethod
    def update(cls, model_type, *filters, update_dict) -> int:
        return cls.get_session().query(model_type).filter(*filters).update(update_dict, synchronize_session=False)

    @classmethod
    def commit(cls, ignore_errors=False):
        try:
            cls.get_session().commit()
        except SQLAlchemyError as e:
            cls.get_session().rollback()
            logging.exception(e)
            if not ignore_errors:
                raise

    @classmethod
    def expunge_all(cls):
        cls.get_session().expunge_all()

    @classmethod
    def flush(cls, object_or_objects=None):
        if object_or_objects is not None and not isinstance(object_or_objects, Iterable):
            object_or_objects = [object_or_objects]
        cls.get_session().flush(objects=object_or_objects)

    @classmethod
    def rollback(cls):
        cls.get_session().rollback()

    @classmethod
    def refresh(cls, model, with_for_update=None):
        return cls.get_session().refresh(model, with_for_update=with_for_update)

    @classmethod
    def refresh_all(cls, models):
        return [cls.refresh(model) for model in models]

    @classmethod
    def close_session(cls):
        session = cls.get_session()
        try:
            # close session, if any model changed, the session will be rollbacked
            session.close()
        except SQLAlchemyError as se:
            logging.exception(se)

    @classmethod
    def remove_session(cls):
        session = cls.get_session()
        try:
            # close session, if any model changed, the session will be rollbacked
            session.close()
        except SQLAlchemyError as se:
            logging.exception(se)
        finally:
            cls.get_instance().session_factory.remove()

    @classmethod
    def extend_query_by(cls, query, *filters, order_by=None, offset=None, limit=None):
        """
        Retrieve results based on a query and filters. Results returned as a list.
        """
        query = query.filter(*filters)
        if order_by is not None:
            if isinstance(order_by, str) and order_by and order_by[0] == '-':
                order_by = desc(order_by[1:])
            query = query.order_by(order_by)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query
