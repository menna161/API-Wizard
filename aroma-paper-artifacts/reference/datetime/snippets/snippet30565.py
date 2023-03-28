import datetime
import decimal
import re
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, Union, cast
from xml.dom.minidom import Document
from xml.dom.minidom import Element as XmlElement
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from ._utils import StreamType, deprecate_with_replacement, deprecation_with_replacement
from .errors import PdfReadError
from .generic import ContentStream, PdfObject


@xmp_metadataDate.setter
def xmp_metadataDate(self, value: datetime.datetime) -> None:
    deprecate_with_replacement('xmp_metadataDate', 'xmp_metadata_date', '4.0.0')
    self.xmp_metadata_date = value
