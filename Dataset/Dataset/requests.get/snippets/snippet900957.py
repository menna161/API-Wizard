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
@patch('spacy_lefff.downloader.tarfile')
def test_downloader(mock_tarfile, mock_get, _tmp_dir):
    content_disposition = 'attachment; filename="model.tar.gz"; filename*=UTF-8model.tar.gz'
    model_tarfile = tarfile.open(os.path.join(_tmp_dir.strpath, 'model.tar.gz'), 'r:gz')
    headers = {'content-disposition': content_disposition, 'content-length': 100000}
    mock_resp = _mock_response(headers=headers)
    mock_get.return_value = mock_resp
    mock_tarfile.open.return_value = model_tarfile
    d = Downloader('test', download_dir=_tmp_dir.strpath, url=URL_MODEL)
    test_folder = os.path.join(_tmp_dir.strpath, 'test')
    m = os.path.join(test_folder, 'model')
    assert (len(_tmp_dir.listdir()) == 2)
    f = io.open(m, mode='r', encoding='utf-8')
    assert (str(f.read()) == 'TEST')
