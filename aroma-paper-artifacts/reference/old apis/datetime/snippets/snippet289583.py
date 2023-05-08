import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


@property
def inactive_datetime(self):
    return self._inactive_datetime
