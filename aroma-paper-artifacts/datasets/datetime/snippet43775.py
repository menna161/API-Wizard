import pytest
from datetime import datetime
from decimal import Decimal
from hive.utils.normalize import block_num, block_date, vests_amount, steem_amount, sbd_amount, parse_amount, amount, legacy_amount, parse_time, utc_timestamp, load_json_key, trunc, rep_log10, safe_img_url, secs_to_str, strtobool, int_log_level


def test_block_date():
    block = dict(timestamp='2018-03-16T10:08:42')
    assert (block_date(block) == datetime(2018, 3, 16, 10, 8, 42))
