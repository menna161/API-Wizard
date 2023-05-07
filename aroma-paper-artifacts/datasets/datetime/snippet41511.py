from base64 import b64decode, b64encode
from datetime import datetime, timezone
from email import utils
from re import findall, fullmatch
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote, unquote as url_unquote
from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name, header_content_split, prettify_header_name, quote, unquote


def __init__(self, my_date: Union[(datetime, str)], **kwargs: Optional[str]):
    '\n        :param my_date: Can either be a datetime that will be automatically converted or a raw string.\n        :param kwargs:\n        '
    super().__init__((utils.format_datetime(my_date.astimezone(timezone.utc), usegmt=True) if (not isinstance(my_date, str)) else my_date), **kwargs)
