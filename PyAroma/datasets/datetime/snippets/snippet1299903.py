import asyncio
import concurrent.futures
import datetime
import functools
import logging
import numbers
import os
import sys
import time
import math
import random
from tornado.concurrent import Future, is_future, chain_future, future_set_exc_info, future_add_done_callback
from tornado.log import app_log
from tornado.util import Configurable, TimeoutError, import_object
import typing
from typing import Union, Any, Type, Optional, Callable, TypeVar, Tuple, Awaitable
from typing import Dict, List
from typing_extensions import Protocol
from tornado.platform.asyncio import AsyncIOLoop
from tornado.platform.asyncio import BaseAsyncIOLoop
from tornado.process import cpu_count
from tornado import gen
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.gen import convert_yielded


def add_timeout(self, deadline: Union[(float, datetime.timedelta)], callback: Callable[(..., None)], *args: Any, **kwargs: Any) -> object:
    "Runs the ``callback`` at the time ``deadline`` from the I/O loop.\n\n        Returns an opaque handle that may be passed to\n        `remove_timeout` to cancel.\n\n        ``deadline`` may be a number denoting a time (on the same\n        scale as `IOLoop.time`, normally `time.time`), or a\n        `datetime.timedelta` object for a deadline relative to the\n        current time.  Since Tornado 4.0, `call_later` is a more\n        convenient alternative for the relative case since it does not\n        require a timedelta object.\n\n        Note that it is not safe to call `add_timeout` from other threads.\n        Instead, you must use `add_callback` to transfer control to the\n        `IOLoop`'s thread, and then call `add_timeout` from there.\n\n        Subclasses of IOLoop must implement either `add_timeout` or\n        `call_at`; the default implementations of each will call\n        the other.  `call_at` is usually easier to implement, but\n        subclasses that wish to maintain compatibility with Tornado\n        versions prior to 4.0 must use `add_timeout` instead.\n\n        .. versionchanged:: 4.0\n           Now passes through ``*args`` and ``**kwargs`` to the callback.\n        "
    if isinstance(deadline, numbers.Real):
        return self.call_at(deadline, callback, *args, **kwargs)
    elif isinstance(deadline, datetime.timedelta):
        return self.call_at((self.time() + deadline.total_seconds()), callback, *args, **kwargs)
    else:
        raise TypeError(('Unsupported deadline %r' % deadline))
