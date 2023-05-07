from base64 import b64decode, b64encode
from datetime import datetime, timezone
from email import utils
from re import findall, fullmatch
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote, unquote as url_unquote
from kiss_headers.models import Header
from kiss_headers.utils import class_to_header_name, header_content_split, prettify_header_name, quote, unquote


def __init__(self, delay_or_date: Union[(datetime, int)], **kwargs: Optional[str]):
    super().__init__((delay_or_date if isinstance(delay_or_date, datetime) else str(delay_or_date)), **kwargs)
