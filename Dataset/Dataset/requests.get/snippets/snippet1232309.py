import base64
import contextlib
import io
from collections import namedtuple, defaultdict
import requests
import pygame


@property
def mp3_data(self):
    if self.__info_modified:
        self.__mp3_data = requests.get((BASE_URL + 'GetVoiceStream/voiceName={}?voiceSpeed={}&inputText={}'.format(self.voice, self.speed, base64.b64encode(self.text.encode()).decode()))).content
        self.__info_modified = False
    return self.__mp3_data
