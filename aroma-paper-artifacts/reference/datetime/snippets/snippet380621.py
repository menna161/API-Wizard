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


def getReports(startTime: datetime) -> List[ReportWrapper]:
    ' Get a list of reports created after the given time '
    ids = getReportIDs(startTime)
    p = Pool(4)
    return p.map(getReport, ids)
