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


def decorator(func):
    if (not _is_enabled):
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        if _context.get().call_stack:
            return func(*args, **kwargs)
        fn_call = FnCall(id=uuid.uuid4().hex, fn_name=_fn_fullname(func), start=datetime.utcnow())
        try:
            return func(*args, **kwargs)
        except Exception:
            (_, exc, traceback) = sys.exc_info()
            fn_call.end = datetime.utcnow()
            ctx = UsageContext()
            ctx.exception = exc
            ctx.traceback = _trace_to_log(traceback)
            ctx.attributes = attrs
            ctx.completed_calls.append(fn_call)
            _produce_event(ctx)
            if traceback:
                raise exc.with_traceback(traceback)
            raise exc
    return wrapper
