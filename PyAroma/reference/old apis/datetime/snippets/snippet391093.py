import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_create_from_payload_and_timestamp() -> None:
    payload = os.urandom(Ksuid.PAYLOAD_LENGTH_IN_BYTES)
    now = datetime.now(tz=timezone.utc)
    now_seconds = now.replace(microsecond=0)
    ksuid = Ksuid(now.timestamp(), payload)
    assert (ksuid.payload == payload)
    assert (ksuid.datetime == now_seconds)
    assert (ksuid.timestamp == now_seconds.timestamp())
