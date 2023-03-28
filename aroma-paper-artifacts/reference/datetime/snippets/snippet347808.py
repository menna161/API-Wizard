import time
import Queue
import datetime
from ark.are.sensor import PullCallbackSensor
from ark.are.client import BaseClient
import ark.are.log as log
import ark.are.config as config
import ark.are.context as context


def query_all(self, time_begin, time_end):
    '\n        根据查询条件，查询出满足条件并且在指定时间范围内的事件文档，如果时间范围跨天，则会针对每一天都进行查询后再将合并的结果返回\n\n        :param int time_begin: 查询筛选的开始时间\n        :param int time_end:  查询筛选的结束时间\n        :return: 事件文档列表\n        :rtype: list\n        '
    begtime = datetime.datetime.fromtimestamp(time_begin)
    endtime = datetime.datetime.fromtimestamp(time_end)
    end_index = endtime.strftime(self._index_tmpl)
    curtime = begtime
    event_all = []
    while True:
        index = curtime.strftime(self._index_tmpl)
        event_all.extend(self.query_perday(index, time_begin, time_end))
        if (index == end_index):
            break
        curtime = (curtime + datetime.timedelta(days=1))
    return event_all
