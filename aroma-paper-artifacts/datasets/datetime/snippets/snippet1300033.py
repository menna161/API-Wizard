import collections
from concurrent.futures import CancelledError
import datetime
import types
from tornado import gen, ioloop
from tornado.concurrent import Future, future_set_result_unless_cancelled
from typing import Union, Optional, Type, Any, Awaitable
import typing
from typing import Deque, Set


def wait(self, timeout: Union[(float, datetime.timedelta)]=None) -> Awaitable[None]:
    'Block until the internal flag is true.\n\n        Returns an awaitable, which raises `tornado.util.TimeoutError` after a\n        timeout.\n        '
    fut = Future()
    if self._value:
        fut.set_result(None)
        return fut
    self._waiters.add(fut)
    fut.add_done_callback((lambda fut: self._waiters.remove(fut)))
    if (timeout is None):
        return fut
    else:
        timeout_fut = gen.with_timeout(timeout, fut, quiet_exceptions=(CancelledError,))
        timeout_fut.add_done_callback((lambda tf: (fut.cancel() if (not fut.done()) else None)))
        return timeout_fut
