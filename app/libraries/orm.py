"""Database classes and functions."""

import sqlalchemy as __sql
import sqlalchemy.orm.session as __sess


# Entity Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *


BaseTable = declarative_base()
SQLITE = 'sqlite'
MSSQL = 'mssql+pyodbc'


def connect_to_engine(path, dialect, *args, **kwargs):
    """Connect to database."""
    if path and dialect:

        return __sql.create_engine(
            '{dialect}://{sqlite}{path}'.format(
                dialect=dialect, path=path,
                sqlite='/' if dialect == SQLITE else ''),
            *args, **kwargs)

    else:
        raise ValueError('[orm - connect_to_engine] Missing Parameters')


def get_session(engine, autoflush=False, autocommit=False, expirecommit=True):
    """Return a session object."""
    session = __sess.sessionmaker(bind=engine, autoflush=autoflush,
                                  autocommit=autocommit,
                                  expire_on_commit=expirecommit)

    return scoped_session(session)


class Adapter():
    """Adapter database class."""

    __engine = None
    __session = None

    def __init__(self, path, dialect):
        """Adapter constructor."""
        self.__engine = connect_to_engine(path, dialect)

    def get(self, mapped_class, ido, *options):
        """Return a database object and session tuple."""
        q, session = self.get_query(mapped_class)

        obj = q.options(options).get(ido) if options else q.get(ido)

        return obj, session

    def exist(self, mapped_class, ido):
        """Return True if exists, otherwise False."""
        return True if self.get(mapped_class, ido)[0] else False

    def get_query(self, *entities, **kwargs):
        """Return query."""
        __session = get_session(self.__engine)

        return __session.query(*entities, **kwargs), __session
