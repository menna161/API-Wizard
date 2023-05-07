import collections
import datetime
import heapq
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from tornado.locks import Event
from typing import Union, TypeVar, Generic, Awaitable
import typing
from typing import Deque, Tuple, List, Any


def _set_timeout(future: Future, timeout: Union[(None, float, datetime.timedelta)]) -> None:
    if timeout:

        def on_timeout() -> None:
            if (not future.done()):
                future.set_exception(gen.TimeoutError())
        io_loop = ioloop.IOLoop.current()
        timeout_handle = io_loop.add_timeout(timeout, on_timeout)
        future.add_done_callback((lambda _: io_loop.remove_timeout(timeout_handle)))
