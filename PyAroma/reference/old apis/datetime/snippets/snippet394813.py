import concurrent.futures
import contextlib
import contextvars
import dataclasses
import hashlib
import logging
import os
import platform
import sys
import typing
import uuid
from datetime import datetime
from functools import wraps
from os.path import expanduser, join
from pathlib import Path
import requests
from feast import flags_helper
from feast.constants import DEFAULT_FEAST_USAGE_VALUE, FEAST_USAGE
from feast.version import get_version


@contextlib.contextmanager
def tracing_span(name):
    '\n    Context manager for wrapping heavy parts of code in tracing span\n    '
    if _is_enabled:
        ctx = _context.get()
        if (not ctx.call_stack):
            raise RuntimeError('tracing_span must be called in usage context')
        last_call = ctx.call_stack[(- 1)]
        fn_call = FnCall(id=uuid.uuid4().hex, parent_id=last_call.id, fn_name=f'{last_call.fn_name}.{name}', start=datetime.utcnow())
    try:
        (yield)
    finally:
        if _is_enabled:
            fn_call.end = datetime.utcnow()
            ctx.completed_calls.append(fn_call)
