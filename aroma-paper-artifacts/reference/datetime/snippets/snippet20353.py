from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from getpass import getpass
from agnostic.mysql import MysqlBackend
from agnostic.postgres import PostgresBackend
from agnostic.sqlite import SqlLiteBackend


def parse_datetime(self, dt):
    if (dt is None):
        return None
    elif isinstance(dt, datetime):
        return dt
    elif isinstance(dt, str):
        try:
            return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
        except:
            return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    else:
        msg = '`{}` must be None or an instance of str or datetime.'
        raise ValueError(repr(dt))
