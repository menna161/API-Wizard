from urllib.request import Request, urlopen
import urllib.parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
from .errors import *


def process_patent_html(self, soup):
    ' Parse patent html using BeautifulSoup module\n\n\n        Returns (variables returned in dictionary, following are key names): \n            - application_number        (str)   : application number\n            - inventor_name             (json)  : inventors of patent \n            - assignee_name_orig        (json)  : original assignees to patent\n            - assignee_name_current     (json)  : current assignees to patent\n            - pub_date                  (str)   : publication date\n            - filing_date               (str)   : filing date\n            - priority_date             (str)   : priority date\n            - grant_date                (str)   : grant date\n            - forward_cites_no_family   (json)  : forward citations that are not family-to-family cites\n            - forward_cites_yes_family  (json)  : forward citations that are family-to-family cites\n            - backward_cites_no_family  (json)  : backward citations that are not family-to-family cites\n            - backward_cites_yes_family (json)  : backward citations that are family-to-family cites\n\n        Inputs:\n            - soup (str) : html string from of google patent html\n            \n\n        '
    try:
        inventor_name = [{'inventor_name': x.get_text()} for x in soup.find_all('dd', itemprop='inventor')]
    except:
        inventor_name = []
    try:
        assignee_name_orig = [{'assignee_name': x.get_text()} for x in soup.find_all('dd', itemprop='assigneeOriginal')]
    except:
        assignee_name_orig = []
    try:
        assignee_name_current = [{'assignee_name': x.get_text()} for x in soup.find_all('dd', itemprop='assigneeCurrent')]
    except:
        assignee_name_current = []
    try:
        pub_date = soup.find('dd', itemprop='publicationDate').get_text()
    except:
        pub_date = ''
    try:
        application_number = soup.find('dd', itemprop='applicationNumber').get_text()
    except:
        application_number = ''
    try:
        filing_date = soup.find('dd', itemprop='filingDate').get_text()
    except:
        filing_date = ''
    list_of_application_events = soup.find_all('dd', itemprop='events')
    priority_date = ''
    grant_date = ''
    for app_event in list_of_application_events:
        try:
            title_info = app_event.find('span', itemprop='type').get_text()
            timeevent = app_event.find('time', itemprop='date').get_text()
            if (title_info == 'priority'):
                priority_date = timeevent
            if (title_info == 'granted'):
                grant_date = timeevent
            if ((title_info == 'publication') and (pub_date == '')):
                pub_date = timeevent
        except:
            continue
    found_forward_cites_orig = soup.find_all('tr', itemprop='forwardReferencesOrig')
    forward_cites_no_family = []
    if (len(found_forward_cites_orig) > 0):
        for citation in found_forward_cites_orig:
            forward_cites_no_family.append(self.parse_citation(citation))
    found_forward_cites_family = soup.find_all('tr', itemprop='forwardReferencesFamily')
    forward_cites_yes_family = []
    if (len(found_forward_cites_family) > 0):
        for citation in found_forward_cites_family:
            forward_cites_yes_family.append(self.parse_citation(citation))
    found_backward_cites_orig = soup.find_all('tr', itemprop='backwardReferences')
    backward_cites_no_family = []
    if (len(found_backward_cites_orig) > 0):
        for citation in found_backward_cites_orig:
            backward_cites_no_family.append(self.parse_citation(citation))
    found_backward_cites_family = soup.find_all('tr', itemprop='backwardReferencesFamily')
    backward_cites_yes_family = []
    if (len(found_backward_cites_family) > 0):
        for citation in found_backward_cites_family:
            backward_cites_yes_family.append(self.parse_citation(citation))
    abstract_text = ''
    if self.return_abstract:
        abstract = soup.find('meta', attrs={'name': 'DC.description'})
        if abstract:
            abstract_text = abstract['content']
    return {'inventor_name': json.dumps(inventor_name), 'assignee_name_orig': json.dumps(assignee_name_orig), 'assignee_name_current': json.dumps(assignee_name_current), 'pub_date': pub_date, 'priority_date': priority_date, 'grant_date': grant_date, 'filing_date': filing_date, 'forward_cite_no_family': json.dumps(forward_cites_no_family), 'forward_cite_yes_family': json.dumps(forward_cites_yes_family), 'backward_cite_no_family': json.dumps(backward_cites_no_family), 'backward_cite_yes_family': json.dumps(backward_cites_yes_family), 'abstract_text': abstract_text}
