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


def processReport(report: ReportWrapper, startTime: datetime) -> Optional[VulnTestInfo]:
    ' Attempt to verify a given report '
    if report.needsBotReply():
        if (startTime > report.getReportedTime()):
            return None
        if config.DEBUG:
            print(('Processing %s' % report.getReportTitle()))
        for module in modules:
            if module.match(report.getReportBody(), report.getReportWeakness()):
                if config.DEBUG:
                    print((module.__file__.split('/')[(- 1)] + (' matched id=%s!' % report.getReportID())))
                vti = module.process(report)
                if config.DEBUGVERBOSE:
                    print(vti)
                if vti:
                    postComment(report.getReportID(), vti, addStopMessage=True)
                    if (vti.reproduced and config.metadataLogging):
                        metadataVTI = generateMetadataVTI(report, vti)
                        postComment(report.getReportID(), metadataVTI, internal=True)
                return vti
        if config.DEBUG:
            print('No matches')
    return None
