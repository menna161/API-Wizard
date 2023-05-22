import base64
import hmac
import inspect
import json
import re
import time
from asyncio import Future
from concurrent.futures import ThreadPoolExecutor as Pool
import tornado.httpserver
import tornado.ioloop
import tornado.web
import yaml
from tornado.ioloop import IOLoop
from yieldbreaker import YieldBreaker
from .scopes import Permission
from .utils import ACCEPT_HEADER_SYMMETRA, Authenticator, add_event, clear_caches
import there
import traceback
import requests
import traceback
import traceback
import traceback
import traceback
import traceback


def fn(req, url):
    try:
        import requests
        headers = {k: req.headers[k] for k in ('content-type', 'User-Agent', 'X-GitHub-Delivery', 'X-GitHub-Event', 'X-Hub-Signature')}
        req = requests.Request('POST', url, headers=headers, data=req.body)
        prepared = req.prepare()
        with requests.Session() as s:
            res = s.send(prepared)
        return res
    except Exception:
        import traceback
        traceback.print_exc()
