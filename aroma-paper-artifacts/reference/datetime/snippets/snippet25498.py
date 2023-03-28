import ftplib
import gzip
import re
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import gmtime, strftime
import click
import decouple


@staticmethod
def parse_timestamp(timestamp):
    'Transforms a timestamp ID in a humanized date'
    date_parsed = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    return date_parsed.strftime('%b %d, %Y at %H:%M:%S')
