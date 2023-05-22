import glob
import numpy
import requests
from io import BytesIO
from PIL import Image


def send_photo(self, photo, caption='', parse_mode='Markdown'):
    try:
        requests.post((self._api_url + '/sendPhoto'), data={'chat_id': self._chat_id, 'caption': caption, 'parse_mode': parse_mode}, files={'photo': self._read_photo(photo)})
    except:
        pass
