import json
from collections import namedtuple
from typing import Generator
import requests
from bs4 import BeautifulSoup


def get_examples(self) -> Generator[(tuple, None, None)]:
    "A generator that gets words' usage examples pairs from server pair by pair.\n\n        Note:\n            Don't try to get all usage examples at one time if there are more than 5 pages (see the total_pages attribute). It\n            may take a long time to complete because it will be necessary to connect to the server as many times as there are pages exist.\n            Just get the usage examples one by one as they are being fetched.\n\n        Yields:\n            Tuples with two WordUsageContext namedtuples (for source and target text and highlighted indexes)\n        "

    def find_highlighted_idxs(soup, tag='em') -> tuple:
        'Finds indexes of the parts of the soup surrounded by a particular HTML tag\n            relatively to the soup without the tag.\n\n            Example:\n                soup = BeautifulSoup("<em>This</em> is <em>a sample</em> string")\n                tag = "em"\n                Returns: [(0, 4), (8, 16)]\n\n            Args:\n                soup: The BeautifulSoup\'s soup.\n                tag: The HTML tag, which surrounds the parts of the soup.\n\n            Returns:\n                  A list of the tuples, which contain start and end indexes of the soup parts,\n                  surrounded by tags.\n\n            '
        (cur, idxs) = (0, [])
        for t in soup.find_all(text=True):
            if (t.parent.name == tag):
                idxs.append((cur, (cur + len(t))))
            cur += len(t)
        return tuple(idxs)
    for npage in range(1, (self.total_pages + 1)):
        self.__data['npage'] = npage
        response = requests.post('https://context.reverso.net/bst-query-service', headers=HEADERS, data=json.dumps(self.__data))
        examples_json = response.json()['list']
        for example in examples_json:
            source = BeautifulSoup(example['s_text'], features='lxml')
            target = BeautifulSoup(example['t_text'], features='lxml')
            (yield (WordUsageContext(source.text, find_highlighted_idxs(source)), WordUsageContext(target.text, find_highlighted_idxs(target))))
