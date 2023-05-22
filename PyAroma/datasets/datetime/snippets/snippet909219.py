import datetime
import re
from typing import Any


def __getattribute__(self, name: str) -> Any:
    if (name == 'default'):
        if ((self._default is None) and (self.auto_now is True)):
            return datetime.datetime.now()
        else:
            return self._default
    return super().__getattribute__(name)
