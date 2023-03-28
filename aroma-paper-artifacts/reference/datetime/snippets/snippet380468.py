import time
from AutoTriageBot.ReportWrapper import ReportWrapper
from AutoTriageBot.sqlite import initDB, countFailures
from AutoTriageBot import config, duplicates, payout, verify
from AutoTriageBot import slack
from AutoTriageBot.modules import modules
import traceback
import datetime
import socket


def run():
    ' Run the bot '
    initDB()
    if config.genesis:
        startTime = config.genesis
    else:
        startTime = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    while True:
        try:
            reports = verify.getReports(startTime)
            if config.DEBUG:
                print(('Found %s reports' % str(len(reports))))
            for (idx, report) in enumerate(reports):
                if config.DEBUGVERBOSE:
                    print(('Processing: %s: %s' % (str(idx), report.getReportTitle())))
                if shouldProcessReport(report):
                    if (not duplicates.processReport(report)):
                        vti = verify.processReport(report, startTime)
                        if (vti and vti.reproduced):
                            payout.processReport(report)
                            try:
                                socket.gethostbyname('slack')
                                slack.postMessage(('<https://hackerone.com/reports/%s|Report #%s> (%s) verified!' % (report.getReportID(), report.getReportID(), report.getReportTitle())), attachments=[{'text': '', 'fallback': '', 'callback_id': ('reportVerified_%s' % report.getReportID()), 'color': '#3AA3E3', 'attachment_type': 'default', 'actions': [{'name': 'metadata', 'text': 'View metadata', 'type': 'button', 'value': 'metadata'}, {'name': 'body', 'text': 'View body', 'type': 'button', 'value': 'body'}]}])
                            except socket.gaierror:
                                slack.postMessage(('<https://hackerone.com/reports/%s|Report #%s> (%s) verified!' % (report.getReportID(), report.getReportID(), report.getReportTitle())))
            if config.DEBUG:
                print('Sleeping...')
            time.sleep(10)
        except Exception as e:
            if config.DEBUG:
                print(('Caught exception: %s' % str(e)))
                traceback.print_exc()
                print(('+' * 80))
