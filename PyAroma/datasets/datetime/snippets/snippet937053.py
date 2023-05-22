import argparse
import collections
import csv
import datetime
import json
import logging
import math
import operator
import os
import re
import sys
import tarfile
import tempfile
import time
import urllib.request as url_req
import xml.etree.cElementTree as xml_et
from datetime import datetime as dts
from datetime import timedelta as dts_delta
from typing import List, Optional
import xmlschema


def _convert_hitrack_timestamp(hitrack_timestamp: float) -> datetime:
    ' Converts the different timestamp formats appearing in HiTrack files to a Python datetime.\n\n    Known formats are seconds (e.g. 1516273200 or 1.5162732E9) or microseconds (e.g. 1516273200000 or 1.5162732E12)\n    '
    timestamp_digits = int(math.log10(hitrack_timestamp))
    if (timestamp_digits == 9):
        return dts.utcfromtimestamp(int(hitrack_timestamp))
    divisor = ((10 ** (timestamp_digits - 9)) if (timestamp_digits > 9) else (0.1 ** (9 - timestamp_digits)))
    return dts.utcfromtimestamp(int((hitrack_timestamp / divisor)))
