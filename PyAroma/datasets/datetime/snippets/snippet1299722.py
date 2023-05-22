import asyncio
import builtins
import collections
from collections.abc import Generator
import concurrent.futures
import datetime
import functools
from functools import singledispatch
from inspect import isawaitable
import sys
import types
from tornado.concurrent import Future, is_future, chain_future, future_set_exc_info, future_add_done_callback, future_set_result_unless_cancelled
from tornado.ioloop import IOLoop
from tornado.log import app_log
from tornado.util import TimeoutError
import typing
from typing import Union, Any, Callable, List, Type, Tuple, Awaitable, Dict
from typing import Sequence, Deque, Optional, Set, Iterable


def with_timeout(timeout: Union[(float, datetime.timedelta)], future: _Yieldable, quiet_exceptions: 'Union[Type[Exception], Tuple[Type[Exception], ...]]'=()) -> Future:
    'Wraps a `.Future` (or other yieldable object) in a timeout.\n\n    Raises `tornado.util.TimeoutError` if the input future does not\n    complete before ``timeout``, which may be specified in any form\n    allowed by `.IOLoop.add_timeout` (i.e. a `datetime.timedelta` or\n    an absolute time relative to `.IOLoop.time`)\n\n    If the wrapped `.Future` fails after it has timed out, the exception\n    will be logged unless it is of a type contained in ``quiet_exceptions``\n    (which may be an exception type or a sequence of types).\n\n    The wrapped `.Future` is not canceled when the timeout expires,\n    permitting it to be reused. `asyncio.wait_for` is similar to this\n    function but it does cancel the wrapped `.Future` on timeout.\n\n    .. versionadded:: 4.0\n\n    .. versionchanged:: 4.1\n       Added the ``quiet_exceptions`` argument and the logging of unhandled\n       exceptions.\n\n    .. versionchanged:: 4.4\n       Added support for yieldable objects other than `.Future`.\n\n    '
    future_converted = convert_yielded(future)
    result = _create_future()
    chain_future(future_converted, result)
    io_loop = IOLoop.current()

    def error_callback(future: Future) -> None:
        try:
            future.result()
        except Exception as e:
            if (not isinstance(e, quiet_exceptions)):
                app_log.error('Exception in Future %r after timeout', future, exc_info=True)

    def timeout_callback() -> None:
        if (not result.done()):
            result.set_exception(TimeoutError('Timeout'))
        future_add_done_callback(future_converted, error_callback)
    timeout_handle = io_loop.add_timeout(timeout, timeout_callback)
    if isinstance(future_converted, Future):
        future_add_done_callback(future_converted, (lambda future: io_loop.remove_timeout(timeout_handle)))
    else:
        io_loop.add_future(future_converted, (lambda future: io_loop.remove_timeout(timeout_handle)))
    return result
