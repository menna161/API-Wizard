from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from getpass import getpass
from agnostic.mysql import MysqlBackend
from agnostic.postgres import PostgresBackend
from agnostic.sqlite import SqlLiteBackend


def __init__(self, name, status, started_at=None, completed_at=None):
    "\n        Constructor.\n\n        The constructor takes arguments in the same order as the table's\n        columns, so it can be instantiated like ``Migration(*row)``, where\n        ``row`` is a row from the table.\n        "
    self.name = name
    if isinstance(status, MigrationStatus):
        self.status = status
    elif isinstance(status, str):
        self.status = MigrationStatus[status]
    else:
        msg = '`status` must be an instance of str or MigrationStatus.'
        raise ValueError(msg)
    self.started_at = self.parse_datetime(started_at)
    self.completed_at = self.parse_datetime(completed_at)
