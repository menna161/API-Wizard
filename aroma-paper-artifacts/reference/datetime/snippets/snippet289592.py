import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


@ordering_datetime.setter
def ordering_datetime(self, value):
    self._ordering_datetime = value
