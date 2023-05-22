from hashlib import md5
import mock
import pytest
from django.utils import six
from localshop.apps.packages import models, tasks
from tests.factories import PackageFactory, ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_with_proxy_enabled(requests_mock, settings):
    settings.LOCALSHOP_HTTP_PROXY = {'http': 'http://10.10.1.10:3128/'}
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None, md5_digest=md5(file_data).hexdigest())
    requests_mock.return_value = mock.Mock(**{'headers': {'content-length': len(file_data), 'content-type': 'application/octet-stream'}, 'content': file_data})
    tasks.download_file.run(release_file.pk)
    requests_mock.assert_called_once_with('http://www.example.org/download/test-1.0.0-sdist.zip', proxies=settings.LOCALSHOP_HTTP_PROXY, stream=True)
