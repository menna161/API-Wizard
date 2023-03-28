from datetime import datetime
from typing import List, Callable, Tuple, Optional, NewType
from urllib.parse import unquote
import json
from AutoTriageBot import AutoTriageUtils
from AutoTriageBot.AutoTriageUtils import VulnTestInfo
from AutoTriageBot.ReportWrapper import ReportWrapper, getLinks
from AutoTriageBot import config
from AutoTriageBot import secrets
from AutoTriageBot.modules import modules
import requests
from requests.auth import HTTPBasicAuth


def getAllOpenReports(time: datetime) -> List[ReportWrapper]:
    ' Get a list of all the open reports '
    reports = [ReportWrapper().deserialize(ser) for ser in json.loads(requests.post('http://api:8080/v1/getReports', auth=HTTPBasicAuth('AutoTriageBot', secrets.apiBoxToken)).text)]
    return list(filter((lambda r: (r.getReportedTime() < time)), filter((lambda r: (r.getState() in ['new', 'triaged', 'needs-more-info'])), reports)))
