from datetime import datetime
from typing import Optional
from cyksuid import hints
from cyksuid._ksuid import BYTE_LENGTH, EMPTY_BYTES, MAX_ENCODED, STRING_ENCODED_LENGTH, Empty, Ksuid
from cyksuid._ksuid import ksuid as _new_ksuid
from cyksuid._ksuid import parse as _new_parse


@property
def datetime(self) -> datetime:
    'Datetime for timestamp (timezone naive).'
    return datetime.utcfromtimestamp(self.timestamp)
