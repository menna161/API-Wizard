import inspect, os
from datetime import datetime
from . import utils
from .app import Jikji
from .app import Jikji
from .app import Jikji


def render_template(template_path, **context):
    ' Render template and return result\n\t'
    from .app import Jikji
    app = Jikji.getinstance()
    if (os.path.splitext(template_path)[1] == ''):
        template_path += '.html'
    context['_page'] = {'url': nowpage().geturl(), 'template': template_path, 'render_time': datetime.now(), 'params': nowpage().params}
    tpl = app.jinja_env.get_template(template_path)
    return tpl.render(context)
