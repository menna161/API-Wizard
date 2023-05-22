from hashlib import md5
import mock
import pytest
from django.utils import six
from localshop.apps.packages import models, tasks
from tests.factories import PackageFactory, ReleaseFileFactory


@mock.patch('requests.get')
@pytest.mark.django_db
def test_download_file_incorrect_md5_sum(requests_mock):
    file_data = six.b('My cool package')
    release_file = ReleaseFileFactory(distribution=None, md5_digest='arcoiro')
    requests_mock.return_value = mock.Mock(**{'headers': {'content-length': len(file_data), 'content-type': 'application/octet-stream'}, 'content': file_data})
    tasks.download_file.run(release_file.pk)
    release_file = models.ReleaseFile.objects.get(pk=release_file.pk)
    assert (not release_file.distribution)
