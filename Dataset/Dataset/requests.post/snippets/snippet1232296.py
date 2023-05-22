import json
from collections import namedtuple
from typing import Generator
import requests
from bs4 import BeautifulSoup


def get_translations(self) -> Generator[(Translation, None, None)]:
    '\n        Yields all available translations for the word.\n\n        While viewing Reverso.Context in a web browser, you can see them in a line just before the examples.\n\n        Yields:\n             Translation namedtuples.\n        '
    response = requests.post('https://context.reverso.net/bst-query-service', headers=HEADERS, data=json.dumps(self.__data))
    translations_json = response.json()['dictionary_entry_list']
    for translation_json in translations_json:
        translation = translation_json['term']
        frequency = translation_json['alignFreq']
        part_of_speech = translation_json['pos']
        inflected_forms = tuple((InflectedForm(form['term'], form['alignFreq']) for form in translation_json['inflectedForms']))
        (yield Translation(self.__data['source_text'], translation, frequency, part_of_speech, inflected_forms))
