import click
import iscc
import iscc_cli
from iscc_cli import fpcalc, ffmpeg
from iscc_cli.const import SUPPORTED_EXTENSIONS
from iscc_cli.tika import tika
import requests


def tika_version():
    url = (tika.ServerEndpoint + '/version')
    try:
        return requests.get(url).text
    except Exception:
        return 'WARNING: Not Installed - run "iscc init" to install!'
