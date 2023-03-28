from django.http import HttpResponse
import datetime
from .utils import get_installed_packages


def test(request):
    now = datetime.datetime.now()
    deps = get_installed_packages()
    return HttpResponse(('<html>\n<body>Hello world!<br/>\n%s<br/>\npath_info: <code>%s</code><br/>\npath: <code>%s</code><br/>\ndeps: <code>%s</code>\n</body>\n</html>' % (now, request.path_info, request.path, deps)))
