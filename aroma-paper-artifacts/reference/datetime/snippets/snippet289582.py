import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


@active_datetime.setter
def active_datetime(self, value):
    self._active_datetime = value
