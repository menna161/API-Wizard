import datetime
import os
import re
import StringIO
import time
import zipfile
from googleapis.codegen.django_helpers import DjangoRenderTemplate
from googleapis.codegen.language_model import LanguageModel
from googleapis.codegen.template_objects import UseableInTemplates
from googleapis.codegen import template_helpers
from googleapis.codegen.filesys import files


def __init__(self):
    super(ToolInformation, self).__init__(_GENERATOR_INFORMATION)
    now = datetime.datetime.utcnow()
    self.SetTemplateValue('runDate', ('%4d-%02d-%02d' % (now.year, now.month, now.day)))
    self.SetTemplateValue('runTime', ('%02d:%02d:%02d UTC' % (now.hour, now.minute, now.second)))
