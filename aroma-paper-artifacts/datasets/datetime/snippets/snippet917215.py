import asyncio
import base64
import logging
import typing
from datetime import datetime
from functools import singledispatch, wraps
from types import GeneratorType
from typing import TypedDict
from typing_extensions import TypedDict


@py2json.register(datetime)
def _(value: datetime):
    return value.isoformat()
