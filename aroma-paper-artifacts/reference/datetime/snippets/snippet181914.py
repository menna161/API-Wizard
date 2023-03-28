import json
from alipay.aop.api.constant.ParamConstants import *


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = AlipayPcreditHuabeiPcreditmerchantProductorderApplyModel()
    if ('active_datetime' in d):
        o.active_datetime = d['active_datetime']
    if ('activity_id' in d):
        o.activity_id = d['activity_id']
    if ('biz_from' in d):
        o.biz_from = d['biz_from']
    if ('extending_info' in d):
        o.extending_info = d['extending_info']
    if ('from_app' in d):
        o.from_app = d['from_app']
    if ('ordered_channel' in d):
        o.ordered_channel = d['ordered_channel']
    if ('ordered_system_code' in d):
        o.ordered_system_code = d['ordered_system_code']
    if ('ordering_datetime' in d):
        o.ordering_datetime = d['ordering_datetime']
    if ('pid' in d):
        o.pid = d['pid']
    if ('ps_code' in d):
        o.ps_code = d['ps_code']
    return o
