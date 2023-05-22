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


def set_connect_timeout(self, connect_timeout: Union[(float, datetime.timedelta)]) -> None:
    self.connect_timeout = self.io_loop.add_timeout(connect_timeout, self.on_connect_timeout)
