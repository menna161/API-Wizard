import os
import pytest
from aao.spiders import SpiderBet365


@pytest.mark.parser
def test_parse_datetime(self, spider):
    spider.soccer._request_page()
    rows = spider.soccer._get_rows()
    for row in rows:
        datetime_str = str(spider.soccer._parse_datetime(row))
        if row[0].isdigit():
            assert (row[0] in datetime_str)
        assert (row[1] in datetime_str)
