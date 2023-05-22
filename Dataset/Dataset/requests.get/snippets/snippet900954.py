import os
import io
import pytest
import tarfile
import tempfile
from mock import patch, Mock, MagicMock
import requests
from spacy_lefff import Downloader
from spacy_lefff.melt_tagger import URL_MODEL


def test_url_model():
    assert (requests.get(URL_MODEL).status_code == 200)
