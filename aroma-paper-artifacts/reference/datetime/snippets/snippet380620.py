from datetime import datetime
from typing import List, Optional
from AutoTriageBot.AutoTriageUtils import postComment, getReport, VulnTestInfo
from AutoTriageBot.ReportWrapper import ReportWrapper
from AutoTriageBot import config
from AutoTriageBot.modules import modules
from AutoTriageBot import secrets
import json
import requests
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool


def getReportIDs(startTime: datetime) -> List[str]:
    ' Get a list of report IDs created after the given time '
    return requests.post('http://api:8080/v1/getReportIDs', json={'time': startTime.isoformat(), 'openOnly': True}, auth=HTTPBasicAuth('AutoTriageBot', secrets.apiBoxToken)).json()
