from __future__ import annotations
import logging
import sys
import weakref
from asyncio import Queue, create_task, get_running_loop, iscoroutine, wait
from datetime import datetime, timezone
from inspect import getmembers, isawaitable
from time import time as stdlib_time
from typing import Any, AsyncIterator, Awaitable, Callable, Generic, List, MutableMapping, Optional, Sequence, Type, TypeVar, cast
from weakref import WeakKeyDictionary
from typeguard import check_argument_types
from asphalt.core.utils import qualified_name
from contextlib import aclosing
from async_generator import aclosing


@property
def utc_timestamp(self) -> datetime:
    '\n        Return a timezone aware :class:`~datetime.datetime` corresponding to the ``time`` variable,\n        using the UTC timezone.\n\n        '
    return datetime.fromtimestamp(self.time, timezone.utc)
