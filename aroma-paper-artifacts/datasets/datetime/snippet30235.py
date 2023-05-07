from dexy.version import DEXY_VERSION
import datetime


def bibtex_text():
    args = {'version': DEXY_VERSION, 'year': datetime.date.today().year}
    return ('@misc{Dexy,\n    title = {Dexy: Reproducible Data Analysis and Document Automation Software, Version~%(version)s},\n    author = {{Nelson, Ana}},\n    year = {%(year)s},\n    url = {http://www.dexy.it/},\n    note = {http://orcid.org/0000-0003-2561-1564}\n}' % args)
