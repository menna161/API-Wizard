import functools
import socket
import numbers
import datetime
import ssl
from tornado.concurrent import Future, future_add_done_callback
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream
from tornado import gen
from tornado.netutil import Resolver
from tornado.platform.auto import set_close_exec
from tornado.gen import TimeoutError
import typing
from typing import Any, Union, Dict, Tuple, List, Callable, Iterator
from typing import Optional, Set


def start(self, timeout: float=_INITIAL_CONNECT_TIMEOUT, connect_timeout: Union[(float, datetime.timedelta)]=None) -> 'Future[Tuple[socket.AddressFamily, Any, IOStream]]':
    self.try_connect(iter(self.primary_addrs))
    self.set_timeout(timeout)
    if (connect_timeout is not None):
        self.set_connect_timeout(connect_timeout)
    return self.future
