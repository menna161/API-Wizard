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


def _produce_event(ctx: UsageContext):
    if (ctx.sampler and (not ctx.sampler.should_record())):
        return
    is_test = (flags_helper.is_test() or bool(({'pytest'} & sys.modules.keys())))
    event = {'timestamp': datetime.utcnow().isoformat(), 'is_test': is_test, 'is_webserver': ((not is_test) and bool(({'uwsgi', 'gunicorn', 'fastapi'} & sys.modules.keys()))), 'calls': [dict(fn_name=c.fn_name, id=c.id, parent_id=c.parent_id, start=(c.start and c.start.isoformat()), end=(c.end and c.end.isoformat())) for c in reversed(ctx.completed_calls)], 'entrypoint': ctx.completed_calls[(- 1)].fn_name, 'exception': (repr(ctx.exception) if ctx.exception else None), 'traceback': (ctx.traceback if ctx.exception else None), **_constant_attributes}
    event.update(ctx.attributes)
    _export(event)
