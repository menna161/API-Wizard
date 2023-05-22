import glob
import numpy
import requests
from io import BytesIO
from PIL import Image


def send_message(self, text, parse_mode='Markdown'):
    try:
        requests.post((self._api_url + '/sendMessage'), data={'chat_id': self._chat_id, 'text': text, 'parse_mode': parse_mode})
    except:
        pass
