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
    'Attempt to lock. Returns an awaitable.\n\n        Returns an awaitable, which raises `tornado.util.TimeoutError` after a\n        timeout.\n        '
    return self._block.acquire(timeout)
