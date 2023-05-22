from .batch_uploader import upload
from .getmeta import getmeta
from .tuploader import tabup
from .zipfiles import zipshape
import argparse
import json
import os
import platform
import re
import subprocess
import sys
import time
import webbrowser
from datetime import datetime
import ee
import pkg_resources
import requests
from logzero import logger
import pipgeo
import gdal
import pandas
from osgeo import gdal


def version_latest(package):
    response = requests.get(f'https://pypi.org/pypi/{package}/json')
    latest_version = response.json()['info']['version']
    return latest_version
