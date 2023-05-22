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
    self.populate_workspace()
    with chdir(self.parent_work_dir()):
        if self.setting('inline-images'):
            self.inline_images(soup)
        if self.setting('inline-styles'):
            self.inline_styles(soup)
    self.output_data.set_data(str(soup))
