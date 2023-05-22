import os
from hashlib import md5
import mock
import pytest
from django.urls import reverse
from django.utils import six
from mock import Mock
from localshop.apps.packages import views
from tests.factories import ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_pypi_release_when_isolated_is_on(requests_mock, rf, repository, settings):
    file_data = six.b('Hello from PyPI')
    md5_digest = md5(file_data).hexdigest()
    settings.LOCALSHOP_ISOLATED = True
    release_file = ReleaseFileFactory(release__package__repository=repository, distribution=None, md5_digest=md5_digest)
    url_kwargs = {'repo': repository.slug, 'name': release_file.release.package.name, 'pk': release_file.pk, 'filename': release_file.filename}
    requests_mock.return_value = Mock(**{'headers': {'content-length': len(file_data), 'content-type': 'application/octet-stream'}, 'content': file_data})
    request = rf.get(reverse('packages:download', kwargs=url_kwargs))
    response = views.DownloadReleaseFile.as_view()(request, **url_kwargs)
    assert (response.status_code == 200)
    assert (response.content == file_data)
    requests_mock.assert_called_with(u'http://www.example.org/download/test-1.0.0-sdist.zip', proxies=None, stream=True)
