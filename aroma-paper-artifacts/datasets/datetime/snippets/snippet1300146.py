import collections
import datetime
import heapq
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from tornado.locks import Event
from typing import Union, TypeVar, Generic, Awaitable
import typing
from typing import Deque, Tuple, List, Any


def join(self, timeout: Union[(float, datetime.timedelta)]=None) -> Awaitable[None]:
    'Block until all items in the queue are processed.\n\n        Returns an awaitable, which raises `tornado.util.TimeoutError` after a\n        timeout.\n        '
    return self._finished.wait(timeout)
