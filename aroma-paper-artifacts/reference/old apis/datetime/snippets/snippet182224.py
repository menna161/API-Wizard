import json
from alipay.aop.api.constant.ParamConstants import *


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = AlipayPcreditHuabeiPcreditmerchantProductorderTransferModel()
    if ('active_datetime' in d):
        o.active_datetime = d['active_datetime']
    if ('extending_info' in d):
        o.extending_info = d['extending_info']
    if ('from_app' in d):
        o.from_app = d['from_app']
    if ('inactive_datetime' in d):
        o.inactive_datetime = d['inactive_datetime']
    if ('inactiving_datetime' in d):
        o.inactiving_datetime = d['inactiving_datetime']
    if ('ordered_channel' in d):
        o.ordered_channel = d['ordered_channel']
    if ('ordered_system_code' in d):
        o.ordered_system_code = d['ordered_system_code']
    if ('ordering_datetime' in d):
        o.ordering_datetime = d['ordering_datetime']
    if ('out_merchant_id' in d):
        o.out_merchant_id = d['out_merchant_id']
    if ('pid' in d):
        o.pid = d['pid']
    if ('ps_code' in d):
        o.ps_code = d['ps_code']
    if ('renew' in d):
        o.renew = d['renew']
    if ('taobao_order_id' in d):
        o.taobao_order_id = d['taobao_order_id']
    return o
