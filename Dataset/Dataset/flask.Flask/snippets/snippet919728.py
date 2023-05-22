import os, shutil
import mimetypes
import flask
import jinja2
from . import utils
from .cprint import cprint
import inspect


def listen(self, port, host):
    ' Start listening HTTP server with Flask\n\t\t'
    cprint.section(('Listening %s pages' % len(self.pages)))
    for (index, url) in enumerate(self.pages):
        if (index > 20):
            cprint.line('...')
            break
        cprint.line(('/' + url))
    cprint.section(('Open Local Server with Flask (%d pages)' % len(self.pages)))
    flaskapp = flask.Flask(__name__)
    flaskapp.add_url_rule('/', 'index', self.response)
    flaskapp.add_url_rule('/__pages', 'list_pages', self.list_pages)
    flaskapp.add_url_rule('/<path:url>', 'response', self.response)
    flaskapp.run(port=port, host=host)
    self.flaskapp = flaskapp
