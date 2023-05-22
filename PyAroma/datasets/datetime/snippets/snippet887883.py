import logging
import random
import uuid
import os
from flask import Blueprint, jsonify, session, request, current_app
from datetime import datetime, timedelta
from decimal import Decimal
from app.api.tree import Tree
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import route, Redis, CaptchaTool, PhoneTool
from app.utils.auth import Auth, login_required
from app.api.report import excel_write, word_write, pdf_write
from app.api.wx_login_or_register import get_access_code, get_wx_user_info, wx_login_or_register
from app.api.phone_login_or_register import SendSms, phone_login_or_register
from app.celery import add, flask_app_context


@route(bp, '/testGetVerificationCode', methods=['GET'])
def test_get_verification_code():
    '\n    获取手机验证码\n    :return:\n    '
    now = datetime.now()
    res = ResMsg()
    category = request.args.get('category', None)
    phone = request.args.get('phone', None)
    re_phone = PhoneTool.check_phone(phone)
    if ((phone is None) or (re_phone is None)):
        res.update(code=ResponseCode.MobileNumberError)
        return res.data
    if (category is None):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    try:
        flag = Redis.hget(re_phone, 'expire_time')
        if (flag is not None):
            flag = datetime.strptime(flag, '%Y-%m-%d %H:%M:%S')
            if ((flag - now).total_seconds() < 60):
                res.update(code=ResponseCode.FrequentOperation)
                return res.data
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        template_param = {'code': code}
        sms = SendSms(phone=re_phone, category=category, template_param=template_param)
        sms.send_sms()
        Redis.hset(re_phone, 'code', code)
        Redis.hset(re_phone, 'expire_time', (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))
        Redis.expire(re_phone, (60 * 3))
        return res.data
    except Exception as e:
        logger.exception(e)
        res.update(code=ResponseCode.Fail)
        return res.data
