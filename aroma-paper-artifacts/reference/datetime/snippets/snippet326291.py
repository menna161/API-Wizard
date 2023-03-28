from __future__ import unicode_literals
from __future__ import absolute_import, division, print_function
import os
import sys
import logging
import subprocess
import importlib
import shutil
import datetime
from annalist import layout
from annalist.identifiers import ANNAL, RDFS
from annalist.util import valid_id, extract_entity_id, make_type_entity_id
from annalist.collections_data import installable_collections
from annalist.models.site import Site
from annalist.models.collection import Collection
from annalist.models.recordtype import RecordType
from annalist.models.recordview import RecordView
from annalist.models.recordlist import RecordList
from annalist.models.recordfield import RecordField
from annalist.models.recordgroup import RecordGroup
from annalist.models.collectiondata import initialize_coll_data, copy_coll_data, migrate_coll_data
from . import am_errors
from .am_settings import am_get_settings, am_get_site_settings, am_get_site
from .am_getargvalue import getarg, getargvalue


def am_installcollection(annroot, userhome, options):
    '\n    Install software-defined collection data\n\n        annalist_manager installcollection coll_id\n\n    Copies data from an existing collection to a new collection.\n\n    annroot     is the root directory for the Annalist software installation.\n    userhome    is the home directory for the host system user issuing the command.\n    options     contains options parsed from the command line.\n\n    returns     0 if all is well, or a non-zero status code.\n                This value is intended to be used as an exit status code\n                for the calling program.\n    '
    (status, settings, site) = get_settings_site(annroot, userhome, options)
    if (status != am_errors.AM_SUCCESS):
        return status
    if (len(options.args) > 1):
        print(('Unexpected arguments for %s: (%s)' % (options.command, ' '.join(options.args))), file=sys.stderr)
        return am_errors.AM_UNEXPECTEDARGS
    coll_id = getargvalue(getarg(options.args, 0), 'Collection Id to install: ')
    if (coll_id in installable_collections):
        src_dir_name = installable_collections[coll_id]['data_dir']
    else:
        print(('Collection name to install not known: %s' % coll_id), file=sys.stderr)
        print(('Available collection Ids are: %s' % ','.join(installable_collections.keys())))
        return am_errors.AM_NOCOLLECTION
    coll = Collection.load(site, coll_id)
    if (coll and coll.get_values()):
        if options.force:
            print(("Existing collection %s will be removed ('--force' specified)" % coll_id), file=sys.stderr)
            Collection.remove(site, coll_id)
        else:
            print(('Collection already exists: %s' % coll_id), file=sys.stderr)
            return am_errors.AM_COLLECTIONEXISTS
    src_dir = os.path.join(annroot, 'annalist/data', src_dir_name)
    print(("Installing collection '%s' from data directory '%s'" % (coll_id, src_dir)))
    coll_metadata = installable_collections[coll_id]['coll_meta']
    date_time_now = datetime.datetime.now().replace(microsecond=0)
    coll_metadata[ANNAL.CURIE.comment] = ('Initialized at %s by `annalist-manager installcollection`' % date_time_now.isoformat())
    coll = site.add_collection(coll_id, coll_metadata)
    msgs = initialize_coll_data(src_dir, coll)
    if msgs:
        for msg in msgs:
            print(msg)
        status = am_errors.AM_INSTALLCOLLFAIL
    return status
