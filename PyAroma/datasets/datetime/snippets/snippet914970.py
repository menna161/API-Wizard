from argparse import ArgumentParser, Namespace
import datetime
import os
from typing import Any, TypedDict, NamedTuple, Union
import hither2 as hi


def _fmt_time(t: Union[(float, None)]) -> str:
    if (not t):
        return 'TIME NOT SPECIFIED'
    return datetime.datetime.fromtimestamp(t).isoformat()
