import json
from alipay.aop.api.constant.ParamConstants import *


def to_alipay_dict(self):
    params = dict()
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
    if self.order_id:
        if hasattr(self.order_id, 'to_alipay_dict'):
            params['order_id'] = self.order_id.to_alipay_dict()
        else:
            params['order_id'] = self.order_id
    if self.pid:
        if hasattr(self.pid, 'to_alipay_dict'):
            params['pid'] = self.pid.to_alipay_dict()
        else:
            params['pid'] = self.pid
    if self.renew_system_code:
        if hasattr(self.renew_system_code, 'to_alipay_dict'):
            params['renew_system_code'] = self.renew_system_code.to_alipay_dict()
        else:
            params['renew_system_code'] = self.renew_system_code
    if self.renewing_datetime:
        if hasattr(self.renewing_datetime, 'to_alipay_dict'):
            params['renewing_datetime'] = self.renewing_datetime.to_alipay_dict()
        else:
            params['renewing_datetime'] = self.renewing_datetime
    return params
