#!/usr/bin/env python3
# pylint: disable=invalid-name
from __future__ import annotations

from datetime import datetime
import inspect

import dateutil
from sqlalchemy import BigInteger, Column, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import func

# Naming convention must be set in order to have names for constraints. Otherwise, alembic downgrade
# will fail when trying remove a unique constraint.

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)
DeclarativeBase = declarative_base(metadata=metadata)


class ModelBase(DeclarativeBase):
    """
    Base class for all models
    """

    __abstract__ = True

    # hack for sqlite, so that sqlite will implement a real autoincrement
    __table_args__ = {
        'sqlite_autoincrement': True,
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
    }

    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        return cls.__name__  # pylint: disable=E0213

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=datetime.utcnow,
        index=True,
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        index=True,
    )

    json = Column(JSON)


def json_property(
    property_name,
    json_field='json',
    default=None,
    property_type=None,
    convert_null=False,
):
    """
    json_property is used to store fields that's not supposed to be indexed, compared or mapping a
    relation.

    In all other cases, create a standalone column instead.
    default:
        Avoid using mutable values, like [] or {}. Leave it empty if you are not sure. It's a
        hybrid_property on JSON field, SQLAlchemy may inject unwanted values.
    """

    callable_default = default if callable(default) else lambda: default

    def getter(self):
        """Field getter"""
        if inspect.isclass(self) and issubclass(self, DeclarativeBase):
            # when used as class property for query
            column = getattr(self, json_field)[property_name]
            return column

        data = getattr(self, json_field) or {}

        value = data.get(property_name, callable_default())

        if property_type is not None and value is not None:
            if isinstance(value, property_type):
                return value

            if property_type is datetime:
                value = datetime.fromtimestamp(value)
            else:
                value = property_type(value)
        if convert_null and value is None:
            return default
        return value

    def setter(self, value):
        """Field setter"""
        if inspect.isclass(self) and issubclass(self, DeclarativeBase):
            # do nothing when used as class property
            return

        if value is not None:
            if property_type is datetime:
                if isinstance(value, datetime):
                    value = value.timestamp()
                elif isinstance(value, str):
                    value = dateutil.parser.parse(value).timestamp()
                else:
                    raise ValueError("Can't set {} to datetime field {}".format(value, property_name))
            elif property_type is not None:
                try:
                    value = property_type(value)
                except Exception as er:
                    raise ValueError(
                        '{property_name} needs {property_type} '
                        'but got {value_type}: {value}'.format(
                            property_name=property_name,
                            property_type=property_type,
                            value_type=type(value),
                            value=value,
                        )
                    ) from er
        if convert_null and value is None:
            value = default

        data = getattr(self, json_field) or {}
        data[property_name] = value
        setattr(self, json_field, data)
        # need to manually tell SQLAlchemy the json_field is modified
        flag_modified(self, json_field)

    def deleter(self):
        """Field deleter"""
        data = getattr(self, json_field) or {}
        if property_name in data:
            del data[property_name]
            setattr(self, json_field, data or None)
            flag_modified(self, json_field)

    return hybrid_property(fget=getter, fset=setter, fdel=deleter)
