import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = ProductOrderDTO()
    if ('active_datetime' in d):
        o.active_datetime = d['active_datetime']
    if ('inactive_datetime' in d):
        o.inactive_datetime = d['inactive_datetime']
    if ('order_id' in d):
        o.order_id = d['order_id']
    if ('order_user_id' in d):
        o.order_user_id = d['order_user_id']
    if ('ordered_channel' in d):
        o.ordered_channel = d['ordered_channel']
    if ('ordering_datetime' in d):
        o.ordering_datetime = d['ordering_datetime']
    if ('out_merchant_id' in d):
        o.out_merchant_id = d['out_merchant_id']
    if ('prod_name' in d):
        o.prod_name = d['prod_name']
    if ('ps_code' in d):
        o.ps_code = d['ps_code']
    if ('sign_activity_dto' in d):
        o.sign_activity_dto = d['sign_activity_dto']
    if ('status' in d):
        o.status = d['status']
    return o
