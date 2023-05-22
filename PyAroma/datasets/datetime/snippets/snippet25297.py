from lxml import etree
from datetime import datetime
import pandas as pd


def data(self, data):
    '\n        Callback function for XMLParser event of data of a tag\n\n        Inputs:\n        - data: String containing the text data for this tag.\n        '
    if (self._in_data_tag == True):
        if self._in_headers:
            if (data == self._last_header):
                self._in_headers = False
                self._header_list.append(data)
                self._in_actual_data = True
                return
            self._header_list.append(data)
            return
        if (data == self._first_header):
            self._in_headers = True
            self._header_list.append(data)
            return
        if self._in_actual_data:
            self._is_possibly_empty = False
            try:
                datetime.strptime(data, '%Y-%m-%d')
                self._curr_date_idx = data
                self._data[self._curr_date_idx] = []
            except ValueError:
                self._data[self._curr_date_idx].append(data)
