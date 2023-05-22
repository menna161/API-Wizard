import json
from alipay.aop.api.constant.ParamConstants import *


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = AlipayPcreditHuabeiPcreditmerchantProductorderDelayModel()
    if ('extending_info' in d):
        o.extending_info = d['extending_info']
    if ('from_app' in d):
        o.from_app = d['from_app']
    if ('order_id' in d):
        o.order_id = d['order_id']
    if ('pid' in d):
        o.pid = d['pid']
    if ('renew_system_code' in d):
        o.renew_system_code = d['renew_system_code']
    if ('renewing_datetime' in d):
        o.renewing_datetime = d['renewing_datetime']
    return o
