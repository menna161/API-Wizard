import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


@inactive_datetime.setter
def inactive_datetime(self, value):
    self._inactive_datetime = value
