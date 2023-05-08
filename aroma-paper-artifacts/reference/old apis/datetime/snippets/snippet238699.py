import json
from alipay.aop.api.constant.ParamConstants import *


@staticmethod
def from_alipay_dict(d):
    if (not d):
        return None
    o = ErrorLog()
    if ('datetime' in d):
        o.datetime = d['datetime']
    if ('error_msg' in d):
        o.error_msg = d['error_msg']
    if ('logon_id' in d):
        o.logon_id = d['logon_id']
    if ('mobile' in d):
        o.mobile = d['mobile']
    if ('trace_id' in d):
        o.trace_id = d['trace_id']
    return o
