import copy
import os
import re
from blockdiag import noderenderer, plugins
from blockdiag.utils import XY, images, unquote, urlutil, uuid
from blockdiag.utils.logging import warning


@classmethod
def find_all(cls):
    for v1 in cls.namespace.values():
        for v2 in v1.values():
            (yield v2)
