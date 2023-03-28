import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_create_from_timestamp() -> None:
    now = datetime.now(tz=timezone.utc)
    now_seconds = now.replace(microsecond=0)
    k: Ksuid = ksuid(time_func=(lambda : now.timestamp()))
    assert (k.datetime == now_seconds)
    assert (k.timestamp == now_seconds.timestamp())
