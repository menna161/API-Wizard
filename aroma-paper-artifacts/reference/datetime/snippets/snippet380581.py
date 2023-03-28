from AutoTriageBot import duplicates
from datetime import datetime
from AutoTriageBot.DataTypes import ReportData
from AutoTriageBot.ReportWrapper import ReportWrapper
import pytest
from AutoTriageBot.tests.testUtils import Counter
from AutoTriageBot.AutoTriageUtils import VulnTestInfo


@pytest.mark.fast
def test_isDuplicate(monkeypatch):
    monkeypatch.setattr(duplicates.AutoTriageUtils.config, 'hostnameSanitizers', {'.*\\.example\\.com': '[server].example.com'})
    na44xss = ReportData(title='XSS Report', body='XSS Report: https://na44.example.com/vulnerable?payload=alert(0)&other=nothing', time=datetime.now(), state='new', id='0', weakness='XSS')
    na43xss_1 = ReportData(title='XSS Report', body='XSS Report: https://na43.example.com/vulnerable?payload=alert(0)&other=nothing', time=datetime.now(), state='new', id='1', weakness='XSS')
    na43xss_2 = ReportData(title='XSS Report', body='XSS Report: https://na43.example.com/vulnerable?payload=alert(0)', time=datetime.now(), state='new', id='1', weakness='XSS')
    na43xss_3 = ReportData(title='XSS Report', body='XSS Report: https://na43.example.com/vulnerable?payload=alert(0)&other=something', time=datetime.now(), state='new', id='2', weakness='XSS')
    otherDomainXss_1 = ReportData(title='XSS Report', body='XSS Report: https://subdomain.example.com/vulnerable?payload=alert(0)&other=something', time=datetime.now(), state='new', id='2', weakness='XSS')
    otherDomainXss_2 = ReportData(title='XSS Report', body='XSS Report: https://subdomain.example.com/vulnerable?payloadDiff=alert(0)&other=something', time=datetime.now(), state='new', id='2', weakness='XSS')
    otherDomainXss_3 = ReportData(title='XSS Report', body='XSS Report: https://subdomain.example.com/vulnerableDiff?payloadDiff=alert(0)&other=something', time=datetime.now(), state='new', id='2', weakness='XSS')
    na44openRedir = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://na44.example.com/vulnerableDir?goTo=https://example.com&other=nothing', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    na43openRedir_1 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://na43.example.com/vulnerableDir?goTo=https://example.com&other=nothing', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    na43openRedir_2 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://na43.example.com/vulnerableDir?goTo=https://example.com', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    na43openRedir_3 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://na43.example.com/vulnerableDir?goTo=https://example.com&other=something', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    otherDomainOpenRedir_1 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://subdomain.example.com/vulnerableDir?goTo=https://example.com&other=something', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    otherDomainOpenRedir_2 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://subdomain.example.com/vulnerableDir?goToDiff=https://example.com&other=something', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    otherDomainOpenRedir_3 = ReportData(title='Open Redirect Report', body='Open Redirect Report: https://subdomain.example.com/vulnerableDirDiff?goToDiff=https://example.com&other=something', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    openRedirNoLinks = ReportData(title='Open Redirect Report', body='Open Redirect Report', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    openRedirLotsOfLinks1 = ReportData(title='Open Redirect Report', body='https://blah1.example.org/1 https://blah2.example.org/2 https://blah3.example.org/3 https://blah4.example.org/4 https://blah5.example.org/5', time=datetime.now(), state='new', id='0', weakness='Open Redirect')
    openRedirLotsOfLinks2 = ReportData(title='Open Redirect Report', body='https://blah11.example.org/11 https://blah22.example.org/22 https://blah33.example.org/33 https://blah44.example.org/44 https://blah55.example.org/55', time=datetime.now(), state='new', id='0', weakness='Open Redirect')

    def rdToRW(r: ReportData) -> ReportWrapper:
        ' Convert a ReportData to a ReportWrapper '
        rw = ReportWrapper()
        monkeypatch.setattr(rw, 'getReportTitle', (lambda : r.title))
        monkeypatch.setattr(rw, 'getReportBody', (lambda : r.body))
        monkeypatch.setattr(rw, 'getReportedTime', (lambda : r.time))
        monkeypatch.setattr(rw, 'getState', (lambda : r.state))
        monkeypatch.setattr(rw, 'getReportID', (lambda : r.id))
        monkeypatch.setattr(rw, 'getReportWeakness', (lambda : r.weakness))
        return rw
    assert (duplicates.isDuplicate(rdToRW(na44xss), rdToRW(na43xss_1))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44xss), rdToRW(na43xss_2))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44xss), rdToRW(na43xss_3))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44xss), rdToRW(na44xss))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na43xss_1), rdToRW(na43xss_3))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(na44xss)) == (None, 'A'))
    assert (duplicates.isDuplicate(rdToRW(otherDomainXss_1), rdToRW(na44xss))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(otherDomainXss_2), rdToRW(na44xss))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(otherDomainXss_3), rdToRW(na44xss))[0] == 90)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(na43openRedir_1))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(na43openRedir_2))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(na43openRedir_3))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(otherDomainOpenRedir_1))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(otherDomainOpenRedir_2))[0] == 99)
    assert (duplicates.isDuplicate(rdToRW(na44openRedir), rdToRW(otherDomainOpenRedir_3))[0] == 90)
    assert (duplicates.isDuplicate(rdToRW(openRedirNoLinks), rdToRW(na44openRedir))[0] is None)
    assert (duplicates.isDuplicate(rdToRW(openRedirLotsOfLinks1), rdToRW(openRedirLotsOfLinks2))[0] == 20)
