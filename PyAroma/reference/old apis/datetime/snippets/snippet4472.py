import pytest
from aao.spiders import SpiderBwin


def test_parse_datetime(self, spider):
    spider.soccer._request_page(events_only=True)
    rows_dict = spider.soccer._get_rows(events_only=True)
    rows = rows_dict['full_time_result']
    for row in rows:
        datetime_str = str(spider.soccer._parse_datetime(row))
        (month, day, year) = row[0].split(' - ')[(- 1)].split('/')
        date = '-'.join([year, month.zfill(2), day.zfill(2)])
        assert (date in datetime_str)
