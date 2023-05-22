import requests
import numpy as np
import cv2
import pytesseract
import re
from datetime import datetime
from bs4 import BeautifulSoup
from apitizer.month_conversion import MONTHS


def fetch_image(self):
    img_url = self.find_image_in_page()
    resp = requests.get((self.url + img_url), stream=True).raw
    resp_data = resp.read()
    if (self.resp_data == resp_data):
        return False
    self.last_update = datetime.now().isoformat()
    self.resp_data = resp_data
    image = np.asarray(bytearray(self.resp_data), dtype='uint8')
    self.image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return True
