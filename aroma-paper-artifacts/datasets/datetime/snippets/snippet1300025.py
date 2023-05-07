import collections
from concurrent.futures import CancelledError
import datetime
import types
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from typing import Union, Optional, Type, Any, Awaitable
import typing
from typing import Deque, Set


def wait(self, timeout: Union[(float, datetime.timedelta)]=None) -> Awaitable[bool]:
    'Wait for `.notify`.\n\n        Returns a `.Future` that resolves ``True`` if the condition is notified,\n        or ``False`` after a timeout.\n        '
    waiter = Future()
    self._waiters.append(waiter)
    if timeout:

        def on_timeout() -> None:
            if (not waiter.done()):
                future_set_result_unless_cancelled(waiter, False)
            self._garbage_collect()
        io_loop = ioloop.IOLoop.current()
        timeout_handle = io_loop.add_timeout(timeout, on_timeout)
        waiter.add_done_callback((lambda _: io_loop.remove_timeout(timeout_handle)))
    return waiter
