from .namespaces import *
import re
import types


def cnv_configtype(attribute, arg, element):
    if (str(arg) not in ('boolean', 'short', 'int', 'long', 'double', 'string', 'datetime', 'base64Binary')):
        raise ValueError(("'%s' not allowed" % str(arg)))
    return str(arg)
