import json
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.SignActivityDTO import SignActivityDTO


def to_alipay_dict(self):
    params = dict()
    if self.active_datetime:
        if hasattr(self.active_datetime, 'to_alipay_dict'):
            params['active_datetime'] = self.active_datetime.to_alipay_dict()
        else:
            params['active_datetime'] = self.active_datetime
    if self.inactive_datetime:
        if hasattr(self.inactive_datetime, 'to_alipay_dict'):
            params['inactive_datetime'] = self.inactive_datetime.to_alipay_dict()
        else:
            params['inactive_datetime'] = self.inactive_datetime
    if self.order_id:
        if hasattr(self.order_id, 'to_alipay_dict'):
            params['order_id'] = self.order_id.to_alipay_dict()
        else:
            params['order_id'] = self.order_id
    if self.order_user_id:
        if hasattr(self.order_user_id, 'to_alipay_dict'):
            params['order_user_id'] = self.order_user_id.to_alipay_dict()
        else:
            params['order_user_id'] = self.order_user_id
    if self.ordered_channel:
        if hasattr(self.ordered_channel, 'to_alipay_dict'):
            params['ordered_channel'] = self.ordered_channel.to_alipay_dict()
        else:
            params['ordered_channel'] = self.ordered_channel
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
    if self.prod_name:
        if hasattr(self.prod_name, 'to_alipay_dict'):
            params['prod_name'] = self.prod_name.to_alipay_dict()
        else:
            params['prod_name'] = self.prod_name
    if self.ps_code:
        if hasattr(self.ps_code, 'to_alipay_dict'):
            params['ps_code'] = self.ps_code.to_alipay_dict()
        else:
            params['ps_code'] = self.ps_code
    if self.sign_activity_dto:
        if hasattr(self.sign_activity_dto, 'to_alipay_dict'):
            params['sign_activity_dto'] = self.sign_activity_dto.to_alipay_dict()
        else:
            params['sign_activity_dto'] = self.sign_activity_dto
    if self.status:
        if hasattr(self.status, 'to_alipay_dict'):
            params['status'] = self.status.to_alipay_dict()
        else:
            params['status'] = self.status
    return params
