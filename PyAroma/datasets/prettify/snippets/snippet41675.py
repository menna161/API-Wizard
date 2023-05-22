from email.header import decode_header
from re import findall, search, sub
from typing import Any, Iterable, List, Optional, Set, Tuple, Type


def prettify_header_name(name: str) -> str:
    '\n    Take a header name and prettify it.\n    >>> prettify_header_name("x-hEllo-wORLD")\n    \'X-Hello-World\'\n    >>> prettify_header_name("server")\n    \'Server\'\n    >>> prettify_header_name("contEnt-TYPE")\n    \'Content-Type\'\n    >>> prettify_header_name("content_type")\n    \'Content-Type\'\n    '
    return '-'.join([el.capitalize() for el in name.replace('_', '-').split('-')])
