from gensim.scripts.glove2word2vec import glove2word2vec
import os
import requests
import tarfile


def download_file_from_google_drive(id, destination):
    URL = 'https://docs.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)
