import datetime
from io import StringIO
import linecache
import os.path
import posixpath
import re
import threading
from tornado import escape
from tornado.log import app_log
from tornado.util import ObjectDict, exec_in, unicode_type
from typing import Any, Union, Callable, List, Dict, Iterable, Optional, TextIO
import typing
from typing import Tuple, ContextManager


def generate(self, **kwargs: Any) -> bytes:
    'Generate this template with the given arguments.'
    namespace = {'escape': escape.xhtml_escape, 'xhtml_escape': escape.xhtml_escape, 'url_escape': escape.url_escape, 'json_encode': escape.json_encode, 'squeeze': escape.squeeze, 'linkify': escape.linkify, 'datetime': datetime, '_tt_utf8': escape.utf8, '_tt_string_types': (unicode_type, bytes), '__name__': self.name.replace('.', '_'), '__loader__': ObjectDict(get_source=(lambda name: self.code))}
    namespace.update(self.namespace)
    namespace.update(kwargs)
    exec_in(self.compiled, namespace)
    execute = typing.cast(Callable[([], bytes)], namespace['_tt_execute'])
    linecache.clearcache()
    return execute()
