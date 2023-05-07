import json
import sys
from typing import Any, Dict, List, TYPE_CHECKING
from datetime import datetime
import copy
import pycountry
import pycountry


@property
def parsed_release_date(self) -> datetime:
    "\n            Returns a datetime representation of the item's release_date. This\n            method is only available when using Python 3.7 or later.\n            "
    return datetime.fromisoformat(self.release_date.replace('Z', '+00:00'))
