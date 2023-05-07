import os
import sys
import io
import re
from datetime import datetime
import math
from . import markdown2
import markdown2


def __init__(self):
    self.title = ''
    self.subject = ''
    self.description = ''
    self.categories = []
    self.duration_sec = 0
    self.keywords = []
    self.date = datetime.now()
    self.authorname = 'Unknown'
    self.authoremail = ''
    self.license = ''
    self.revisionstr = '0'
    self.tags = []
    self.points = None
    self.prio = 0
    self.versionstr = '0.0.0'
    self.releaseversion = False
