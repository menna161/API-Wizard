import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_ms_mode_datetime() -> None:
    time = datetime.now()

    def fix_timestamp_precision(timestamp: float) -> float:
        timestamp_ms = int((timestamp * 1000))
        s = (timestamp_ms // 1000)
        ms = ((timestamp_ms % 1000) >> 2)
        ms = ((ms << 2) % 1000)
        return (((s * 1000) + ms) / 1000)
    for i in range(TEST_ITEMS_COUNT):
        k = ksuid(time_func=(lambda : time.timestamp()), ksuid_cls=KsuidMs)
        assert (fix_timestamp_precision(time.timestamp()) == k.timestamp)
        time += timedelta(milliseconds=5)
