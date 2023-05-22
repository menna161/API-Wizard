import json
from alipay.aop.api.constant.ParamConstants import *


def to_alipay_dict(self):
    params = dict()
    if self.datetime:
        if hasattr(self.datetime, 'to_alipay_dict'):
            params['datetime'] = self.datetime.to_alipay_dict()
        else:
            params['datetime'] = self.datetime
    if self.error_msg:
        if hasattr(self.error_msg, 'to_alipay_dict'):
            params['error_msg'] = self.error_msg.to_alipay_dict()
        else:
            params['error_msg'] = self.error_msg
    if self.logon_id:
        if hasattr(self.logon_id, 'to_alipay_dict'):
            params['logon_id'] = self.logon_id.to_alipay_dict()
        else:
            params['logon_id'] = self.logon_id
    if self.mobile:
        if hasattr(self.mobile, 'to_alipay_dict'):
            params['mobile'] = self.mobile.to_alipay_dict()
        else:
            params['mobile'] = self.mobile
    if self.trace_id:
        if hasattr(self.trace_id, 'to_alipay_dict'):
            params['trace_id'] = self.trace_id.to_alipay_dict()
        else:
            params['trace_id'] = self.trace_id
    return params
