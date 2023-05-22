import time
import asyncio
import itertools
import datetime as dt
from typing import Callable
import pytest
import ayo
from ayo.scope import ExecutionScope
from ayo.utils import LazyTask


def test_max_concurrency(count):
    'setting a timeout limit the time it can execute in '

    async def foo():
        start = dt.datetime.now()
        (await asyncio.sleep(0.1))
        return start

    def diff_in_seconds(x, y):
        return abs(round((x.timestamp() - y.timestamp()), 1))

    @ayo.run_as_main()
    async def main1(run):
        async with ayo.scope(max_concurrency=2) as runalso:
            runalso.all(foo(), foo(), foo(), foo(), foo(), foo())
        (a, b, c, d, e, f) = runalso.results
        assert (diff_in_seconds(a, b) == 0.0)
        assert (diff_in_seconds(c, d) == 0.0)
        assert (diff_in_seconds(e, f) == 0.0)
        assert (diff_in_seconds(c, b) == 0.1)
        assert (diff_in_seconds(d, e) == 0.1)

    @ayo.run_as_main(max_concurrency=2)
    async def main2(run):
        results = run.all(foo(), foo(), foo(), foo(), foo(), foo()).gather()
        (a, b, c, d, e, f) = (await results)
        assert (diff_in_seconds(a, b) == 0.0)
        assert (diff_in_seconds(c, d) == 0.0)
        assert (diff_in_seconds(e, f) == 0.0)
        assert (diff_in_seconds(c, b) == 0.1)
        assert (diff_in_seconds(d, e) == 0.1)

    @ayo.run_as_main()
    async def main3(run):
        async with ayo.scope(max_concurrency=2) as runalso:
            runalso.from_callable(foo)
            runalso.from_callable(foo)
            runalso.from_callable(foo)
            runalso.from_callable(foo)
            runalso.from_callable(foo)
            runalso.from_callable(foo)
        (a, b, c, d, e, f) = runalso.results
        assert (diff_in_seconds(a, b) == 0.0)
        assert (diff_in_seconds(c, d) == 0.0)
        assert (diff_in_seconds(e, f) == 0.0)
        assert (diff_in_seconds(c, b) == 0.1)
        assert (diff_in_seconds(d, e) == 0.1)
