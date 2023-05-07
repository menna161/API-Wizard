import pytest
from datetime import datetime
from decimal import Decimal
from hive.utils.normalize import block_num, block_date, vests_amount, steem_amount, sbd_amount, parse_amount, amount, legacy_amount, parse_time, utc_timestamp, load_json_key, trunc, rep_log10, safe_img_url, secs_to_str, strtobool, int_log_level


def test_parse_time():
    block_time = '2018-06-22T20:34:30'
    assert (parse_time(block_time) == datetime(2018, 6, 22, 20, 34, 30))
