from abc import ABCMeta, abstractmethod
from datetime import datetime


def key(conn):
    return (datetime.min if (conn.backoff_time is None) else conn.backoff_time)
