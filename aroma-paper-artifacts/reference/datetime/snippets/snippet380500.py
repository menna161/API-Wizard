from typing import NewType, Mapping, List, Union, cast, Optional
from urllib.parse import urlparse
import json
from copy import deepcopy
from datetime import datetime
import arrow
import re
import ast
from AutoTriageBot import config


def parseTime(timeStr: str) -> datetime:
    ' Parse the given time string into a datetime '
    return arrow.get(timeStr).datetime
