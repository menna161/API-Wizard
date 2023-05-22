import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_timestamp_uniqueness() -> None:
    time = datetime.now()
    ksuids_set: Set[Ksuid] = set()
    for i in range(TEST_ITEMS_COUNT):
        ksuids_set.add(Ksuid(time.timestamp(), EMPTY_KSUID_PAYLOAD))
        time += timedelta(seconds=1)
    assert (len(ksuids_set) == TEST_ITEMS_COUNT)
