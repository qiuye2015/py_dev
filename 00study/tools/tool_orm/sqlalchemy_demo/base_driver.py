#!/usr/bin/env python3
class BaseDriver:
    """Base class for a database driver"""

    @classmethod
    def create_engine(cls):
        pass

    @classmethod
    def create_extra_engines(cls):
        pass

    @classmethod
    def map_column_type(cls):
        pass
