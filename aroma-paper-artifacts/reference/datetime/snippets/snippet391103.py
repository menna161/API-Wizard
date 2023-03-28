import json
import os
from datetime import datetime, timedelta, timezone
from typing import Set
import pytest
from cyksuid.v2 import Ksuid, KsuidMs, from_bytes, ksuid, parse


def test_golib_interop_ms_mode() -> None:
    tf_path = os.path.join(TESTS_DIR, 'test_ksuids.txt')
    with open(tf_path, 'r') as test_kuids:
        lines = test_kuids.readlines()
        for ksuid_json in lines:
            test_data = json.loads(ksuid_json)
            ksuid = Ksuid(test_data['timestamp'], bytes.fromhex(test_data['payload']))
            n = KsuidMs.PAYLOAD_LENGTH_IN_BYTES
            ksuid_ms = KsuidMs(ksuid.datetime.timestamp(), ksuid.payload[:n])
            assert (ksuid_ms.datetime == ksuid.datetime)
            ksuid_ms_from = KsuidMs(ksuid_ms.datetime.timestamp(), ksuid_ms.payload)
            assert (ksuid_ms.payload == ksuid_ms_from.payload)
            assert (ksuid_ms.timestamp == ksuid_ms_from.timestamp)
            ksuid_ms = parse(test_data['ksuid'], ksuid_cls=KsuidMs)
            timediff = (ksuid_ms.datetime - ksuid.datetime)
            assert (abs((timediff.total_seconds() * (10 ** 3))) <= 1000)
            assert (test_data['ksuid'] == str(ksuid_ms))
