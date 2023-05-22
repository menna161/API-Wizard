import os, json, time, requests, html, threading, queue
from xml.etree import ElementTree as ETree
import datetime
import itchat
from itchat.content import *
import signal
import timeout_decorator


def talk(self, info):
    if ((self.apikey is None) or (self.apiurl is None)):
        return None
    data = {'reqType': 0, 'perception': {'inputText': {'text': info.lower()}}, 'userInfo': {'apiKey': self.apikey, 'userId': '0'}}
    try:
        req = requests.post(self.apiurl, data=json.dumps(data), timeout=5).text
        results = json.loads(req)['results']
        for group in results:
            if (group['resultType'] == 'text'):
                txt = group['values']['text']
                if (txt.find(u'不知道') >= 0):
                    return None
                if (txt.find(u'不会') >= 0):
                    return None
                if (txt.find(u'抱歉') >= 0):
                    return None
                return txt
    except:
        return None
