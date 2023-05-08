import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_payload_uniqueness() -> None:
    now = datetime.now()
    timestamp = now.replace(microsecond=0).timestamp()
    ksuids_set: Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(ksuid(time_func=(lambda : now.timestamp())))
    assert (len(ksuids_set) == TEST_ITEMS_COUNT)
    for k in ksuids_set:
        assert (k.timestamp == timestamp)
