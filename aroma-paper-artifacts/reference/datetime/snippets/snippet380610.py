import pytest
from AutoTriageBot.ReportWrapper import ReportWrapper
import datetime
from AutoTriageBot.tests.testUtils import Counter
from AutoTriageBot.DataTypes import VulnTestInfo
from AutoTriageBot.ReportWrapper import extractJson
from AutoTriageBot import verify
from AutoTriageBot import verify


@pytest.mark.fast
def test_verifyProcess(monkeypatch):
    from AutoTriageBot import verify
    time = datetime.datetime.now()
    monkeypatch.setattr(verify, 'postComment', Counter())
    report = ReportWrapper()
    monkeypatch.setattr(report, 'needsBotReply', (lambda : False))
    assert (verify.postComment.count == 0)
    assert (verify.processReport(report, time) is None)
    assert (verify.postComment.count == 0)
    monkeypatch.setattr(report, 'needsBotReply', (lambda : True))
    monkeypatch.setattr(report, 'getReportedTime', (lambda : datetime.datetime.now()))
    monkeypatch.setattr(verify.config, 'genesis', datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc))
    monkeypatch.setattr(verify.config, 'DEBUG', False)
    monkeypatch.setattr(report, 'getReportBody', (lambda : 'XSS report'))
    monkeypatch.setattr(report, 'getReportTitle', (lambda : 'XSS report'))
    monkeypatch.setattr(report, 'getReportWeakness', (lambda : 'XSS'))
    monkeypatch.setattr(report, 'getReportID', (lambda : '-1'))
    vti = VulnTestInfo(reproduced=False, message='VTI', info={}, type='type')
    for module in verify.modules:
        monkeypatch.setattr(module, 'process', (lambda r: vti))
        monkeypatch.setattr(module, 'match', (lambda u, v: True))
    monkeypatch.setattr(report, 'needsBotReply', (lambda : True))
    assert report.needsBotReply()
    assert (verify.postComment.count == 0)
    assert (verify.processReport(report, time) == vti)
    assert (verify.postComment.count == 1)
    assert (verify.postComment.lastCall == (('-1', vti), {'addStopMessage': True}))
    for module in verify.modules:
        monkeypatch.setattr(module, 'match', (lambda b, w: False))
    assert (verify.postComment.count == 1)
    assert (verify.processReport(report, time) is None)
    assert (verify.postComment.count == 1)
