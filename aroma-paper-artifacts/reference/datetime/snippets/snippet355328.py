from __future__ import annotations
import gc
from asyncio import AbstractEventLoop, Queue, all_tasks, current_task
from datetime import datetime, timedelta, timezone
from typing import NoReturn
import pytest
from async_generator import aclosing
from asphalt.core import Event, Signal, stream_events, wait_event


def test_utc_timestamp(self, source: DummySource) -> None:
    timestamp = datetime.now(timezone(timedelta(hours=2)))
    event = Event(source, 'sometopic', timestamp.timestamp())
    assert (event.utc_timestamp == timestamp)
    assert (event.utc_timestamp.tzinfo == timezone.utc)
