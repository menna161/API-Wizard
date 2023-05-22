from .exc import IncludeError, GenerateError
import requests
from requests.exceptions import InvalidSchema
from inspect import isgenerator
from rowgenerators import get_generator


def find_decl_doc(self, name):
    raise IncludeError(name)
    import requests
    from requests.exceptions import InvalidSchema
    url = ((METATAB_ASSETS_URL + name) + '.csv')
    try:
        r = requests.head(url, allow_redirects=False)
        if (r.status_code == requests.codes.ok):
            return url
    except InvalidSchema:
        pass
