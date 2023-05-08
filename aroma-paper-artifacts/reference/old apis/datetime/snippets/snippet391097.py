import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_compare() -> None:
    now = datetime.now()
    k: Ksuid = ksuid(time_func=(lambda : now.timestamp()))
    k_older: Ksuid = ksuid(time_func=(lambda : (now - timedelta(hours=1)).timestamp()))
    assert (k > k_older)
    assert (not (k_older > k))
    assert (k != k_older)
    assert (not (k == k_older))
