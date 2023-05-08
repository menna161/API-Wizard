from typing import NewType, Mapping, List, Union, cast, Optional
from urllib.parse import urlparse
import json
from copy import deepcopy
from datetime import datetime
import arrow
import re
import ast
from AutoTriageBot import config


def getReportedTime(self) -> datetime:
    ' Get the time the report was created at '
    assert isinstance(self.reportedTime, datetime)
    return self.reportedTime
