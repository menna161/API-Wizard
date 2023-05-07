import collections
import datetime
import heapq
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from tornado.locks import Event
from typing import Union, TypeVar, Generic, Awaitable
import typing
from typing import Deque, Tuple, List, Any


def put(self, item: _T, timeout: Union[(float, datetime.timedelta)]=None) -> 'Future[None]':
    'Put an item into the queue, perhaps waiting until there is room.\n\n        Returns a Future, which raises `tornado.util.TimeoutError` after a\n        timeout.\n\n        ``timeout`` may be a number denoting a time (on the same\n        scale as `tornado.ioloop.IOLoop.time`, normally `time.time`), or a\n        `datetime.timedelta` object for a deadline relative to the\n        current time.\n        '
    future = Future()
    try:
        self.put_nowait(item)
    except QueueFull:
        self._putters.append((item, future))
        _set_timeout(future, timeout)
    else:
        future.set_result(None)
    return future
