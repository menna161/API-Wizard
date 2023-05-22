import requests
from . import get_library


def test_links():
    'Ensure that our all links are working.\n    '
    for entry in get_library():
        for k in ('homepage', 'url'):
            link = entry[k]
            r = requests.head(link)
            assert (r.status_code in (200, 302)), link
