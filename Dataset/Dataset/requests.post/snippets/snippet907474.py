import os
import smtplib
import time
import xml.etree.ElementTree as ET
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from click import echo, style
from jinja2 import Template
import requests
from .exceptions import SendDingTalkFailException
from .config_manager import v, EmailReportConfig, DingTalkReportConfig


def send_ding_talk_msg(hook_url, project_name, test_result):
    '\n    发送钉钉消息\n    :param project_name: 项目名称\n    :param hook_url: 回调地址\n    :param test_result: 测试结果\n    '
    pass_pic_url = 'https://s1.ax1x.com/2020/06/25/NwjUG6.png'
    fail_pic_url = 'https://s1.ax1x.com/2020/06/27/NyoprQ.png'
    msg = {'msgtype': 'link', 'link': {'title': ('%s TEST %s' % (project_name.upper(), test_result['test_result'])), 'text': ('总用例数：%s\n失败用例：%s\n运行耗时：%ss' % (test_result['total_case_num'], (test_result['total_failed_case_num'] + test_result['total_error_case_num']), test_result['run_duration_time'])), 'picUrl': (pass_pic_url if (test_result['test_result'] == 'SUCCESS') else fail_pic_url), 'messageUrl': 'http://'}}
    res = requests.post(hook_url, json=msg).json()
    if (res['errcode'] > 0):
        raise SendDingTalkFailException(('发送钉钉消息失败，失败原因：%s' % res['errmsg']))
