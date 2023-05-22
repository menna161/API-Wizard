import json
from alipay.aop.api.constant.ParamConstants import *


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = AlipayPcreditHuabeiPcreditmerchantProductorderSignModel()
    if ('category' in d):
        o.category = d['category']
    if ('due_type' in d):
        o.due_type = d['due_type']
    if ('from_app' in d):
        o.from_app = d['from_app']
    if ('inactive_datetime' in d):
        o.inactive_datetime = d['inactive_datetime']
    if ('industry' in d):
        o.industry = d['industry']
    if ('ordered_channel' in d):
        o.ordered_channel = d['ordered_channel']
    if ('ordered_system_code' in d):
        o.ordered_system_code = d['ordered_system_code']
    if ('out_merchant_id' in d):
        o.out_merchant_id = d['out_merchant_id']
    if ('pid' in d):
        o.pid = d['pid']
    if ('ps_code' in d):
        o.ps_code = d['ps_code']
    if ('shop_name' in d):
        o.shop_name = d['shop_name']
    if ('shop_type' in d):
        o.shop_type = d['shop_type']
    if ('sign_scene' in d):
        o.sign_scene = d['sign_scene']
    return o
