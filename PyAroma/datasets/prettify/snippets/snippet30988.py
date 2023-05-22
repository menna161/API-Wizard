from dexy.doc import Doc
from dexy.filters.templating import TemplateFilter
from dexy.filters.templating_plugins import TemplatePlugin
from tests.utils import wrap
from dexy.exceptions import UserFeedback


def test_jinja_filters_bs4():
    data = run_jinja_filter("{{ '<p>foo</p>' | prettify_html }}")
    assert (str(data) == '<p>\n foo\n</p>')
