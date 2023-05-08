from __future__ import unicode_literals
from __future__ import absolute_import, division, print_function
import logging
import os.path
import shutil
import datetime
from django.conf import settings
from utils.py3porting import isoformat_space
from annalist import layout
from annalist.util import replacetree, removetree
from annalist.collections_data import installable_collections
from annalist.identifiers import ANNAL, RDFS
from annalist.models.site import Site
from annalist.models.collection import Collection
from annalist.models.annalistuser import AnnalistUser
from annalist.models.recordtype import RecordType
from annalist.models.recordview import RecordView
from annalist.models.recordlist import RecordList
from annalist.models.recordfield import RecordField
from annalist.models.recordvocab import RecordVocab
from annalist.models.recordtypedata import RecordTypeData
from annalist.models.entitydata import EntityData
from annalist.models.collectiondata import initialize_coll_data, copy_coll_data, migrate_coll_data
from .entity_testutils import collection_create_values
from .entity_testtypedata import recordtype_create_values
from .tests import test_layout, TestHost, TestHostUri, TestBasePath, TestBaseUri, TestBaseDir


def install_annalist_named_coll(coll_id):
    coll_src_dir = installable_collections[coll_id]['data_dir']
    site = Site(TestBaseUri, TestBaseDir)
    src_dir = os.path.join(settings.SITE_SRC_ROOT, 'annalist/data', coll_src_dir)
    log.debug(("Installing collection '%s' from data directory '%s'" % (coll_id, src_dir)))
    coll_metadata = installable_collections[coll_id]['coll_meta']
    datetime_now = datetime.datetime.now().replace(microsecond=0)
    coll_metadata[ANNAL.CURIE.comment] = ('Initialized at %s by `annalist.tests.init_tests.install_annalist_named_coll`' % isoformat_space(datetime_now))
    coll = site.add_collection(coll_id, coll_metadata)
    msgs = initialize_coll_data(src_dir, coll)
    if msgs:
        for msg in msgs:
            log.warning(msg)
        assert False, '\n'.join(msgs)
    return coll
