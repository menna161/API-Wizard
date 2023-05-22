import requests
import lxml.html as htmlparser
import re
import os
from utils import parse_args, mkdir
from wordsRepoProc import build_wordrepo


def get_page(url, word):
    '\n    get the translation webpage\n    :param url:\n    :param word:\n    :return webpage:\n    '
    queryUrl = (url + word)
    response = requests.get(queryUrl)
    return response.content
