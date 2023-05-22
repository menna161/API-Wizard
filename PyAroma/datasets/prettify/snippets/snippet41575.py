from copy import deepcopy
from json import dumps
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Type, Union
from kiss_headers.structures import AttributeBag, CaseInsensitiveDict
from kiss_headers.utils import escape_double_quote, extract_comments, header_content_split, header_name_to_class, is_legal_header_name, normalize_list, normalize_str, prettify_header_name, unescape_double_quote, unfold, unpack_protected_keyword, unquote


def __init__(self, name: str, content: str):
    '\n        :param name: The name of the header, should contain only ASCII characters with no spaces in it.\n        :param content: Initial content associated with the header.\n        '
    if (not is_legal_header_name(name)):
        raise ValueError(f"'{name}' is not a valid header name. Cannot proceed with it.")
    self._name: str = name
    self._normalized_name: str = normalize_str(self._name)
    self._pretty_name: str = prettify_header_name(self._name)
    self._content: str = content
    self._members: List[str] = header_content_split(self._content, ';')
    self._attrs: Attributes = Attributes(self._members)
