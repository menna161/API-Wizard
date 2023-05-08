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
        ctx = _context.get()
        ctx.call_stack.append(FnCall(id=uuid.uuid4().hex, parent_id=(ctx.call_stack[(- 1)].id if ctx.call_stack else None), fn_name=_fn_fullname(func), start=datetime.utcnow()))
        ctx.attributes.update(attrs)
        try:
            return func(*args, **kwargs)
        except Exception:
            if ctx.exception:
                raise
            (_, exc, traceback) = sys.exc_info()
            ctx.exception = exc
            ctx.traceback = _trace_to_log(traceback)
            if traceback:
                raise exc.with_traceback(traceback)
            raise exc
        finally:
            ctx.sampler = (sampler if (sampler.priority > ctx.sampler.priority) else ctx.sampler)
            last_call = ctx.call_stack.pop((- 1))
            last_call.end = datetime.utcnow()
            ctx.completed_calls.append(last_call)
            if ((not ctx.call_stack) or ((len(ctx.call_stack) == 1) and ('feast.feature_store.FeatureStore.serve' in str(ctx.call_stack[0].fn_name)))):
                _produce_event(ctx)
                clear_context(ctx)
    return wrapper
