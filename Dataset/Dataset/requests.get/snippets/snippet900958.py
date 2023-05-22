import os
import io
import pytest
import tarfile
import tempfile
from mock import patch, Mock, MagicMock
import requests
from spacy_lefff import Downloader
from spacy_lefff.melt_tagger import URL_MODEL


@patch('spacy_lefff.downloader.requests.get')
def test_downloader_failed(mock_get, _tmp_dir):
    mock_resp = _mock_response()
    mock_get.return_value = mock_resp
    with pytest.raises(Exception) as e_info:
        d = Downloader('test', download_dir=_tmp_dir.strpath, url='')
        assert (e_info.value.message == "Couldn't fetch model data.")
