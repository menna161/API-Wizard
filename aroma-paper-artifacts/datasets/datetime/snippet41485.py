from email.message import Message
from email.parser import HeaderParser
from io import BufferedReader, RawIOBase
from json import dumps as json_dumps, loads as json_loads
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Type, TypeVar, Union
from kiss_headers.models import Header, Headers
from kiss_headers.serializer import decode, encode
from kiss_headers.structures import CaseInsensitiveDict
from kiss_headers.utils import class_to_header_name, decode_partials, extract_class_name, extract_encoded_headers, header_content_split, header_name_to_class, is_legal_header_name, normalize_str


def get_polymorphic(target: Union[(Headers, Header)], desired_output: Type[T]) -> Union[(T, List[T], None)]:
    'Experimental. Transform a Header or Headers object to its target `CustomHeader` subclass\n    to access more ready-to-use methods. eg. You have a Header object named \'Set-Cookie\' and you wish\n    to extract the expiration date as a datetime.\n    >>> header = Header("Set-Cookie", "1P_JAR=2020-03-16-21; expires=Wed, 15-Apr-2020 21:27:31 GMT")\n    >>> header["expires"]\n    \'Wed, 15-Apr-2020 21:27:31 GMT\'\n    >>> from kiss_headers import SetCookie\n    >>> set_cookie = get_polymorphic(header, SetCookie)\n    >>> set_cookie.get_expire()\n    datetime.datetime(2020, 4, 15, 21, 27, 31, tzinfo=datetime.timezone.utc)\n    '
    if (not issubclass(desired_output, Header)):
        raise TypeError(f'The desired output should be a subclass of Header not {desired_output}.')
    desired_output_header_name: str = class_to_header_name(desired_output)
    if isinstance(target, Headers):
        r = target.get(desired_output_header_name)
        if (r is None):
            return None
    elif isinstance(target, Header):
        if (header_name_to_class(target.name, Header) != desired_output):
            raise TypeError(f'The target class does not match the desired output class. {target.__class__} != {desired_output}.')
        r = target
    else:
        raise TypeError(f'Unable to apply get_polymorphic on type {target.__class__}.')
    if (not isinstance(r, list)):
        r.__class__ = desired_output
    else:
        for header in r:
            header.__class__ = desired_output
    return r
