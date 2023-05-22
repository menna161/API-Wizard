import json
from alipay.aop.api.constant.ParamConstants import *


def to_alipay_dict(self):
    params = dict()
    if self.category:
        if hasattr(self.category, 'to_alipay_dict'):
            params['category'] = self.category.to_alipay_dict()
        else:
            params['category'] = self.category
    if self.due_type:
        if hasattr(self.due_type, 'to_alipay_dict'):
            params['due_type'] = self.due_type.to_alipay_dict()
        else:
            params['due_type'] = self.due_type
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
    if self.industry:
        if hasattr(self.industry, 'to_alipay_dict'):
            params['industry'] = self.industry.to_alipay_dict()
        else:
            params['industry'] = self.industry
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
    if self.shop_name:
        if hasattr(self.shop_name, 'to_alipay_dict'):
            params['shop_name'] = self.shop_name.to_alipay_dict()
        else:
            params['shop_name'] = self.shop_name
    if self.shop_type:
        if hasattr(self.shop_type, 'to_alipay_dict'):
            params['shop_type'] = self.shop_type.to_alipay_dict()
        else:
            params['shop_type'] = self.shop_type
    if self.sign_scene:
        if hasattr(self.sign_scene, 'to_alipay_dict'):
            params['sign_scene'] = self.sign_scene.to_alipay_dict()
        else:
            params['sign_scene'] = self.sign_scene
    return params
