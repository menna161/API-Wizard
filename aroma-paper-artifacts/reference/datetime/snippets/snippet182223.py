import json
from alipay.aop.api.constant.ParamConstants import *


def to_alipay_dict(self):
    params = dict()
    if self.active_datetime:
        if hasattr(self.active_datetime, 'to_alipay_dict'):
            params['active_datetime'] = self.active_datetime.to_alipay_dict()
        else:
            params['active_datetime'] = self.active_datetime
    if self.extending_info:
        if hasattr(self.extending_info, 'to_alipay_dict'):
            params['extending_info'] = self.extending_info.to_alipay_dict()
        else:
            params['extending_info'] = self.extending_info
    if self.from_app:
        if hasattr(self.from_app, 'to_alipay_dict'):
            params['from_app'] = self.from_app.to_alipay_dict()
        else:
            params['from_app'] = self.from_app
    if self.inactive_datetime:
        if hasattr(self.inactive_datetime, 'to_alipay_dict'):
            params['inactive_datetime'] = self.inactive_datetime.to_alipay_dict()
        else:
            params['inactive_datetime'] = self.inactive_datetime
    if self.inactiving_datetime:
        if hasattr(self.inactiving_datetime, 'to_alipay_dict'):
            params['inactiving_datetime'] = self.inactiving_datetime.to_alipay_dict()
        else:
            params['inactiving_datetime'] = self.inactiving_datetime
    if self.ordered_channel:
        if hasattr(self.ordered_channel, 'to_alipay_dict'):
            params['ordered_channel'] = self.ordered_channel.to_alipay_dict()
        else:
            params['ordered_channel'] = self.ordered_channel
    if self.ordered_system_code:
        if hasattr(self.ordered_system_code, 'to_alipay_dict'):
            params['ordered_system_code'] = self.ordered_system_code.to_alipay_dict()
        else:
            params['ordered_system_code'] = self.ordered_system_code
    if self.ordering_datetime:
        if hasattr(self.ordering_datetime, 'to_alipay_dict'):
            params['ordering_datetime'] = self.ordering_datetime.to_alipay_dict()
        else:
            params['ordering_datetime'] = self.ordering_datetime
    if self.out_merchant_id:
        if hasattr(self.out_merchant_id, 'to_alipay_dict'):
            params['out_merchant_id'] = self.out_merchant_id.to_alipay_dict()
        else:
            params['out_merchant_id'] = self.out_merchant_id
    if self.pid:
        if hasattr(self.pid, 'to_alipay_dict'):
            params['pid'] = self.pid.to_alipay_dict()
        else:
            params['pid'] = self.pid
    if self.ps_code:
        if hasattr(self.ps_code, 'to_alipay_dict'):
            params['ps_code'] = self.ps_code.to_alipay_dict()
        else:
            params['ps_code'] = self.ps_code
    if self.renew:
        if hasattr(self.renew, 'to_alipay_dict'):
            params['renew'] = self.renew.to_alipay_dict()
        else:
            params['renew'] = self.renew
    if self.taobao_order_id:
        if hasattr(self.taobao_order_id, 'to_alipay_dict'):
            params['taobao_order_id'] = self.taobao_order_id.to_alipay_dict()
        else:
            params['taobao_order_id'] = self.taobao_order_id
    return params
