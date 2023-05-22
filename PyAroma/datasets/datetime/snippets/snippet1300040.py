import collections
from concurrent.futures import CancelledError
import datetime
import types
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from typing import Union, Optional, Type, Any, Awaitable
import typing
from typing import Deque, Set


def acquire(self, timeout: Union[(float, datetime.timedelta)]=None) -> Awaitable[_ReleasingContextManager]:
    'Decrement the counter. Returns an awaitable.\n\n        Block if the counter is zero and wait for a `.release`. The awaitable\n        raises `.TimeoutError` after the deadline.\n        '
    waiter = Future()
    if (self._value > 0):
        self._value -= 1
        waiter.set_result(_ReleasingContextManager(self))
    else:
        self._waiters.append(waiter)
        if timeout:

            def on_timeout() -> None:
                if (not waiter.done()):
                    waiter.set_exception(gen.TimeoutError())
                self._garbage_collect()
            io_loop = ioloop.IOLoop.current()
            timeout_handle = io_loop.add_timeout(timeout, on_timeout)
            waiter.add_done_callback((lambda _: io_loop.remove_timeout(timeout_handle)))
    return waiter
