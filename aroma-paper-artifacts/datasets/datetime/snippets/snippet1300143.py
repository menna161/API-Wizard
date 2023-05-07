import collections
import datetime
import heapq
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from tornado.locks import Event
from typing import Union, TypeVar, Generic, Awaitable
import typing
from typing import Deque, Tuple, List, Any


def get(self, timeout: Union[(float, datetime.timedelta)]=None) -> Awaitable[_T]:
    "Remove and return an item from the queue.\n\n        Returns an awaitable which resolves once an item is available, or raises\n        `tornado.util.TimeoutError` after a timeout.\n\n        ``timeout`` may be a number denoting a time (on the same\n        scale as `tornado.ioloop.IOLoop.time`, normally `time.time`), or a\n        `datetime.timedelta` object for a deadline relative to the\n        current time.\n\n        .. note::\n\n           The ``timeout`` argument of this method differs from that\n           of the standard library's `queue.Queue.get`. That method\n           interprets numeric values as relative timeouts; this one\n           interprets them as absolute deadlines and requires\n           ``timedelta`` objects for relative timeouts (consistent\n           with other timeouts in Tornado).\n\n        "
    future = Future()
    try:
        future.set_result(self.get_nowait())
    except QueueEmpty:
        self._getters.append(future)
        _set_timeout(future, timeout)
    return future
