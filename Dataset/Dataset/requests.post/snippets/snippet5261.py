import enum
import json
import logging
import os
import re
import time
from typing import Generator, BinaryIO, Iterable
import requests
from bs4 import BeautifulSoup as Soup
from bs4 import element
from saucenao import http
from saucenao.exceptions import *


def __check_image(self, file_object: BinaryIO, output_type: int) -> str:
    'Check the possible sources for the given file object\n\n        :type output_type: int\n        :type file_object: typing.BinaryIO\n        :return:\n        '
    (files, params, headers) = self.__get_http_data(file_object=file_object, output_type=output_type)
    link = requests.post(url=self.SEARCH_POST_URL, files=files, params=params, headers=headers)
    (code, msg) = http.verify_status_code(link)
    if (code == http.STATUS_CODE_SKIP):
        self.logger.error(msg)
        return json.dumps({'results': []})
    elif (code == http.STATUS_CODE_REPEAT):
        if (not self.previous_status_code):
            self.previous_status_code = code
            self.logger.info('Received an unexpected status code (message: {msg}), repeating after 10 seconds...'.format(msg=msg))
            time.sleep(10)
            return self.__check_image(file_object, output_type)
        else:
            raise UnknownStatusCodeException(msg)
    else:
        self.previous_status_code = None
    if (output_type == self.API_HTML_TYPE):
        return self.parse_results_html_to_json(link.text)
    return link.text
