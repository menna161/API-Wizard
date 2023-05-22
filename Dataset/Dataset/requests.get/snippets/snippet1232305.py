import base64
import contextlib
import io
from collections import namedtuple, defaultdict
import requests
import pygame


@staticmethod
def __get_voices():
    voices = defaultdict(list)
    response = requests.get((BASE_URL + 'GetAvailableVoices'))
    voices_json = response.json()
    for voice_json in voices_json['Voices']:
        language_name = voice_json['Language']
        (name, langcode, gender) = (voice_json['Name'], int(voice_json['LangCode']), voice_json['Gender'])
        voice = Voice(name, (langcode, language_name), gender)
        voices[language_name].append(voice)
    return dict(voices)
