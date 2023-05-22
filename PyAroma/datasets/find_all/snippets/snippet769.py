from __future__ import division, print_function, absolute_import, unicode_literals
import requests
from bs4 import BeautifulSoup


def gen_adaptor(mission):
    r = requests.get(url, params={'mission': mission})
    if (r.status_code != requests.codes.ok):
        r.raise_for_status()
    tree = BeautifulSoup(r.content)
    table_body = tree.find_all('tbody')
    assert (table_body is not None)
    for row in table_body[0].find_all('tr'):
        (short_name, long_name, desc, ex, t) = row.find_all('td')
        print('"{0}": ("{1}", {2}),'.format(long_name.text.strip(), short_name.text.strip(), types[t.text.strip()]))
