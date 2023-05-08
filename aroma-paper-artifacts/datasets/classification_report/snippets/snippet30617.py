from bs4 import BeautifulSoup
from dexy.filter import DexyFilter
from dexy.utils import chdir
import base64
import inflection
import mimetypes
import re
import urllib


def process(self):
    soup = BeautifulSoup(str(self.input_data), self.setting('html-parser'))
    for tag in soup.find_all(re.compile('^h[0-6]')):
        name = tag.text
        m = re.match('^h([0-6])$', tag.name)
        if (not ('id' in tag.attrs)):
            tag.attrs['id'] = inflection.parameterize(name)
        self.current_section_anchor = tag.attrs['id']
        self.current_section_text = None
        self.current_section_name = name
        self.current_section_level = int(m.groups()[0])
        self.append_current_section()
    self.current_section_text = str(soup)
    self.current_section_name = self.setting('initial-section-name')
    self.current_section_level = 1
    self.current_section_anchor = None
    self.append_current_section()
    self.output_data.save()
