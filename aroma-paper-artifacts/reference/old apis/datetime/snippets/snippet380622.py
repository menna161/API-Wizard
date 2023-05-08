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


def generateMetadataVTI(report: ReportWrapper, vti: VulnTestInfo) -> VulnTestInfo:
    ' Given the results of a vulnerability test thar reproduced a vulnerability and a report, generate an internal\n        VTI used to hold metadata about the vulnerability '
    internalMetadata = {'id': report.getReportID(), 'title': report.getReportTitle(), 'reportedTime': str(report.getReportedTime()), 'verifiedTime': str(datetime.now()), 'type': vti.type, 'exploitURL': vti.info['src'], 'method': vti.info['method']}
    if (vti.type == 'XSS'):
        internalMetadata['confirmedBrowsers'] = vti.info['confirmedBrowsers']
        internalMetadata['alertBrowsers'] = vti.info['alertBrowsers']
        internalMetadata['httpType'] = vti.info['httpType']
        internalMetadata['cookies'] = vti.info['cookies']
    elif (vti.type == 'SQLi'):
        internalMetadata['delay'] = vti.info['delay']
        internalMetadata['httpType'] = vti.info['httpType']
        internalMetadata['cookies'] = vti.info['cookies']
    elif (vti.type == 'Open Redirect'):
        internalMetadata['redirect'] = vti.info['redirect']
        internalMetadata['httpType'] = vti.info['httpType']
        internalMetadata['cookies'] = vti.info['cookies']
    message = ('# Internal Metadata: \n\n```\n%s\n```\n' % json.dumps(internalMetadata, sort_keys=True, indent=4, separators=(',', ': ')))
    if config.DEBUGVERBOSE:
        print(internalMetadata)
    internalVTI = VulnTestInfo(reproduced=False, message=message, info={}, type='')
    return internalVTI
