import time
import datetime
from aiocron import asyncio
from aiocron import crontab
import pytest


def test_next_dst(monkeypatch):
    now = datetime.datetime.now()

    class mydatetime():

        @classmethod
        def now(cls, tzinfo=None):
            return datetime.datetime(2018, 10, 29, 2, 58, 58, tzinfo=tzinfo)
    monkeypatch.setattr('aiocron.datetime', mydatetime)
    monkeypatch.setattr('dateutil.tz.time.timezone', (- 3600))
    monkeypatch.setattr('dateutil.tz.time.altzone', (- 7200))
    monkeypatch.setattr('dateutil.tz.time.daylight', 1)
    monkeypatch.setattr('dateutil.tz.time.tzname', ('CET', 'CEST'))
    loop = asyncio.new_event_loop()
    t = crontab('* * * * *', loop=loop)
    t.initialize()
    a = t.get_next()
    time.sleep(3)
    b = t.get_next()
    assert (int((b - a)) == 60)
