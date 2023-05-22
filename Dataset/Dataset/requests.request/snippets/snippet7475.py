import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def __init__(self, request: requests.request):
    if (self.__class__ is RecipeSite):
        raise NotImplementedError('Do not initialize this class. Inherit from it, instead.')
    self.request = request
    self.soup = BeautifulSoup(request.text, 'lxml')
