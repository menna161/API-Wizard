import os
import re
import struct
import zlib
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union, cast
from ._encryption import Encryption, PasswordType
from ._page import PageObject, _VirtualList
from ._page_labels import index2label as page_index2page_label
from ._utils import StrByteType, StreamType, b_, deprecate_no_replacement, deprecation_no_replacement, deprecation_with_replacement, logger_warning, read_non_whitespace, read_previous_line, read_until_whitespace, skip_over_comment, skip_over_whitespace
from .constants import CatalogAttributes as CA
from .constants import CatalogDictionary as CD
from .constants import CheckboxRadioButtonAttributes
from .constants import Core as CO
from .constants import DocumentInformationAttributes as DI
from .constants import FieldDictionaryAttributes, GoToActionArguments
from .constants import PageAttributes as PG
from .constants import PagesAttributes as PA
from .constants import TrailerKeys as TK
from .errors import EmptyFileError, FileNotDecryptedError, PdfReadError, PdfStreamError, WrongPasswordError
from .generic import ArrayObject, ContentStream, DecodedStreamObject, Destination, DictionaryObject, EncodedStreamObject, Field, Fit, FloatObject, IndirectObject, NameObject, NullObject, NumberObject, PdfObject, TextStringObject, TreeObject, read_object
from .types import OutlineType, PagemodeType
from .xmp import XmpInformation


@property
def creation_date(self) -> Optional[datetime]:
    "Read-only property accessing the document's creation date."
    text = self._get_text(DI.CREATION_DATE)
    if (text is None):
        return None
    return datetime.strptime(text.replace("'", ''), 'D:%Y%m%d%H%M%S%z')
