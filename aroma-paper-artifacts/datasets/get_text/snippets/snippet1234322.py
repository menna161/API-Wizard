from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdevice import PDFDevice
import io
import pdfminer
import unicodedata
import json


def parseObj(newScript, lt_objs, pageHeight):
    for obj in lt_objs:
        if isinstance(obj, pdfminer.layout.LTTextLine):
            newScript['pdf'][(- 1)]['content'].append({'x': round(obj.bbox[0]), 'y': round((pageHeight - obj.bbox[1])), 'text': obj.get_text().replace('\n', '').strip()})
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            parseObj(newScript, obj._objs, pageHeight)
