import datetime
import time
import pytest
from cyksuid import ksuid


def test_construct_from_timestamp() -> None:
    cur_time = time.time()

    def time_func() -> float:
        return cur_time
    x = ksuid.ksuid(time_func=time_func)
    assert (x.datetime == datetime.datetime.utcfromtimestamp(int(cur_time)))
