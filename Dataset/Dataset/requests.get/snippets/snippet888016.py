from hashlib import md5
import mock
import pytest
from django.utils import six
from localshop.apps.packages import models, tasks
from tests.factories import PackageFactory, ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_missing_content_length(requests_mock, settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None, md5_digest=md5(file_data).hexdigest())
    requests_mock.return_value = mock.Mock(**{'headers': {'content-type': 'application/octet-stream'}, 'content': file_data})
    tasks.download_file.run(release_file.pk)
    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
    assert (release_file.distribution.read() == file_data)
    assert (release_file.distribution.size == len(file_data))
    assert (release_file.distribution.name == 'default/2.7/t/test-package/test-1.0.0-sdist.zip')
