'''
Created on Dec 11, 2012

@author: sdepedro
'''

import sqlalchemy as __sql
import sqlalchemy.orm.session as __sess


# Entity Base
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import *

BaseTable = declarative_base()
SQLITE = 'sqlite'
MSSQL = 'mssql+pyodbc'


def connect_to_engine(path, dialect, *args, **kwargs):
    if path and dialect:

        return __sql.create_engine(
            '{dialect}://{sqlite}{path}'.format(dialect=dialect, path=path, sqlite='/' if dialect == SQLITE else ''),
            *args, **kwargs)

    else:
        raise ValueError('[orm - connect_to_engine] Missing Parameters')


def get_session(engine, auto_flush=False, autocommit=False, expire_on_commit=True):
    session = __sess.sessionmaker(bind=engine, autoflush=auto_flush, autocommit=autocommit,
                                  expire_on_commit=expire_on_commit)

    return scoped_session(session)


class Adapter():
    __engine = None
    __session = None

    def __init__(self, path, dialect):
        self.__engine = connect_to_engine(path, dialect)

    def get(self, mapped_class, ido, *options):

        q, session = self.get_query(mapped_class)

        obj = q.options(options).get(ido) if options else q.get(ido)

        return obj, session

    def exist(self, mapped_class, ido):
        return True if self.get(mapped_class, ido)[0] else False

    def get_query(self, *entities, **kwargs):
        __session = get_session(self.__engine)

        return __session.query(*entities, **kwargs), __session

