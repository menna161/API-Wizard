import time
import datetime
from aiocron import asyncio
from aiocron import crontab
import pytest


@classmethod
def now(cls, tzinfo=None):
    return datetime.datetime(2018, 10, 29, 2, 58, 58, tzinfo=tzinfo)
