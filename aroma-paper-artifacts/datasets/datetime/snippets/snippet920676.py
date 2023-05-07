import asyncio
import base64
import binascii
import cgi
import datetime
import functools
import inspect
import netrc
import os
import platform
import re
import sys
import time
import warnings
import weakref
from collections import namedtuple
from contextlib import suppress
from math import ceil
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Pattern, Set, Tuple, Type, TypeVar, Union, cast
from urllib.parse import quote
from urllib.request import getproxies
import async_timeout
import attr
from multidict import MultiDict, MultiDictProxy
from yarl import URL
from . import hdrs
from .log import client_logger, internal_logger
from .typedefs import PathLike
import idna_ssl
from typing import ContextManager
from ._helpers import reify as reify_c
from typing_extensions import ContextManager


def next_whole_second() -> datetime.datetime:
    'Return current time rounded up to the next whole second.'
    return (datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + datetime.timedelta(seconds=0))
