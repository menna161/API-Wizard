from typing import NewType, Mapping, List, Union, cast, Optional
from urllib.parse import urlparse
import json
from copy import deepcopy
from datetime import datetime
import arrow
import re
import ast
from AutoTriageBot import config


def _getCommentTime(self, commentJson: CommentJSON) -> datetime:
    ' Get the time the given comment was posted '
    return parseTime(cast(str, commentJson['time']))
