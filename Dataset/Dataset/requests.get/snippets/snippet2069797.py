import requests
import time
import json
import re
import logging, os, sys
from ..utils import SSH


def _request(self, url, method=requests.get, data=None, headers=None, retry_when_response_unexpected_strings=None, retry_until_response_expected_strings=None):
    if (not headers):
        headers = self._headers
    mustend = (time.time() + 1800)
    while (time.time() < mustend):
        res = method((self.endpoint + url), headers=headers, data=json.dumps(data))
        self.log.info('REQUEST: token/{}, {} {}, status/{}'.format(self._token, method.__name__, url, res.status_code))
        if retry_when_response_unexpected_strings:
            ss = list(filter((lambda x: (x in res.text)), retry_when_response_unexpected_strings))
            if ss:
                self.log.info('REQUEST RETRING, AS UNEXPECTED RESPONSE STRING "{}" appeared in response: "{}"!'.format(ss[0], res.text))
                time.sleep(5)
                continue
        if retry_until_response_expected_strings:
            ss = list(filter((lambda x: (x in res.text)), retry_until_response_expected_strings))
            if (not ss):
                self.log.info('REQUEST RETRING, AS EXPECTED RESPONSE STRING "{}"  didn\'t appear in response: "{}"!'.format(' or '.join(retry_until_response_expected_strings), res.text))
                time.sleep(5)
                continue
        break
    if (not res.ok):
        raise Exception(res.status_code, res.text)
    try:
        if res.text:
            return res.json()
    except Exception as e:
        print(type(e), e)
