import json
import requests
from pyplan.pyplan.common.baseService import BaseService


def updateMessage(self, id):
    try:
        msg_url = f'https://ping.pyplan.com/msg/{id}'
        requests.patch(url=msg_url)
    except Exception as ex:
        pass
