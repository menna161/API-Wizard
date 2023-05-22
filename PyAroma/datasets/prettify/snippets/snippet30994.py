from dexy.doc import Doc
from dexy.filters.templating import TemplateFilter
from dexy.filters.templating_plugins import TemplatePlugin
from tests.utils import wrap
from dexy.exceptions import UserFeedback


def test_jinja_filters_combined():
    data = run_jinja_filter("{{ '<p>foo</p>' | prettify_html | highlight('html') }}")
    assert (str(data) == '<div class="highlight"><pre><span></span><a name="l-1"></a><span class="p">&lt;</span><span class="nt">p</span><span class="p">&gt;</span>\n<a name="l-2"></a> foo\n<a name="l-3"></a><span class="p">&lt;/</span><span class="nt">p</span><span class="p">&gt;</span>\n</pre></div>\n')
