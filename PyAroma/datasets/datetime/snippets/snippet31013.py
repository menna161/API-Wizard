from dexy.doc import Doc
from dexy.filters.templating import TemplateFilter
from dexy.filters.templating_plugins import TemplatePlugin
from tests.utils import run_templating_plugin as run
from tests.utils import wrap
import dexy.filters.templating_plugins as plugin
import inspect
import os


def test_python_datetime():
    with run(plugin.PythonDatetime) as env:
        assert inspect.ismodule(env['cal'][1])
