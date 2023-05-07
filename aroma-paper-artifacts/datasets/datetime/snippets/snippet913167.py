import os
import sys
import io
import subprocess
from datetime import datetime
from PyQt5.QtXml import QDomDocument
from .durradocument import DURRADocument


def loadDocument(self, document):
    self._document = document
    info = self.getDocumentInfoFromDocument(self._document)
    self._filename_kra = self._document.fileName()
    self._filename_name = os.path.splitext(self._filename_kra)[0]
    self.title = info['title']
    self.subject = info['subject']
    self.categories = [info['subject']]
    self.description = info['description']
    self.keywords = info['keyword'].split(';')
    self.license = info['license']
    self.duration_sec = int((info['editingtimestr'] if info['editingtimestr'] else 0))
    self.authorname = info['authorname']
    self.date = datetime.strptime(info['datestr'], '%Y-%m-%dT%H:%M:%S')
    self.authoremail = info['authoremail']
    self.revisionstr = info['revisionstr']
    verarr = self.getVERSIONArr()
    if (verarr and (len(verarr) >= 3)):
        if (verarr[0] > 0):
            self.releaseversion = True
        elif (verarr[1] > int(self.revisionstr)):
            newversionstr = (('0.' + self.revisionstr) + '.0')
            self.versionstr = newversionstr
