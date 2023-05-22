from base64 import b64decode, b64encode
from datetime import datetime, timezone
from email import utils
from re import findall, fullmatch
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote, unquote as url_unquote
from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name, header_content_split, prettify_header_name, quote, unquote


def __init__(self, initial_content: str='', **kwargs: Optional[str]):
    '\n        :param initial_content: Initial content of the Header if any.\n        :param kwargs: Provided args. Any key that associate a None value are just ignored.\n        '
    if (self.__class__ == CustomHeader):
        raise NotImplementedError('You can not instantiate CustomHeader class. You may create first your class that inherit it.')
    super().__init__((class_to_header_name(self.__class__) if (not self.__class__.__override__) else prettify_header_name(self.__class__.__override__)), initial_content)
    for (attribute, value) in kwargs.items():
        if (value is None):
            continue
        self[attribute] = value
