from Acquire.Client import FileMeta as _FileMeta
from copy import copy as _copy
from Acquire.Client import Authorisation as _Authorisation
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Client import ChunkUploader as _ChunkUploader
from Acquire.Client import Authorisation as _Authorisation
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.Client import FileMeta as _FileMeta
from Acquire.Storage import FileHandle as _FileHandle
from Acquire.Client import ChunkDownloader as _ChunkDownloader
from Acquire.Client import create_new_file as _create_new_file
from Acquire.Client import FileMeta as _FileMeta
from Acquire.ObjectStore import string_to_list as _string_to_list
from Acquire.Storage import FileMeta as _FileMeta
from Acquire.Client import StorageCreds as _StorageCreds
from copy import copy as _copy
from Acquire.Crypto import get_private_key as _get_private_key
from Acquire.Crypto import get_private_key as _get_private_key
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Crypto import get_private_key as _get_private_key
from Acquire.Client import Authorisation as _Authorisation
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import DriveMeta as _DriveMeta
from Acquire.Client import uncompress as _uncompress
from Acquire.ObjectStore import OSPar as _OSPar
from Acquire.Crypto import get_private_key as _get_private_key
from Acquire.Client import uncompress as _uncompress
from Acquire.Client import ChunkDownloader as _ChunkDownloader


def download(self, filename=None, version=None, dir=None, force_par=False):
    "Download this file into the local directory\n           the local directory, or 'dir' if specified,\n           calling the file 'filename' (or whatever it is called\n           on the Drive if not specified). If a local\n           file exists with this name, then a new, unique filename\n           will be used. This returns the local filename of the\n           downloaded file (with full absolute path)\n\n           Note that this only downloads files for which you\n           have read-access. If the file is not readable then\n           an exception is raised and nothing is returned\n\n           If 'version' is specified then download a specific version\n           of the file. Otherwise download the version associated\n           with this file object\n        "
    if self.is_null():
        raise PermissionError('Cannot download a null File!')
    if (self._creds is None):
        raise PermissionError('We have not properly opened the file!')
    if (filename is None):
        filename = self._metadata.name()
    drive_uid = self._metadata.drive().uid()
    from Acquire.Client import create_new_file as _create_new_file
    if self._creds.is_user():
        privkey = self._creds.user().session_key()
    else:
        from Acquire.Crypto import get_private_key as _get_private_key
        privkey = _get_private_key('parkey')
    args = {'drive_uid': drive_uid, 'filename': self._metadata.name(), 'encryption_key': privkey.public_key().to_data()}
    if self._creds.is_user():
        from Acquire.Client import Authorisation as _Authorisation
        authorisation = _Authorisation(resource=('download %s %s' % (drive_uid, self._metadata.name())), user=self._creds.user())
        args['authorisation'] = authorisation.to_data()
    elif self._creds.is_par():
        par = self._creds.par()
        par.assert_valid()
        args['par_uid'] = par.uid()
        args['secret'] = self._creds.secret()
    if force_par:
        args['force_par'] = True
    if (version is not None):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        args['version'] = _datetime_to_string(version)
    elif (self._metadata.version() is not None):
        args['version'] = self._metadata.version()
    storage_service = self._creds.storage_service()
    response = storage_service.call_function(function='download', args=args)
    from Acquire.Client import FileMeta as _FileMeta
    filemeta = _FileMeta.from_data(response['filemeta'])
    if ('filedata' in response):
        filedata = response['filedata']
        from Acquire.ObjectStore import string_to_bytes as _string_to_bytes
        filedata = _string_to_bytes(response['filedata'])
        del response['filedata']
        filemeta.assert_correct_data(filedata)
        if filemeta.is_compressed():
            from Acquire.Client import uncompress as _uncompress
            filedata = _uncompress(inputdata=filedata, compression_type=filemeta.compression_type())
        filename = _create_new_file(filename=filename, dir=dir)
        with open(filename, 'wb') as FILE:
            FILE.write(filedata)
            FILE.flush()
    elif ('download_par' in response):
        from Acquire.ObjectStore import OSPar as _OSPar
        filename = _create_new_file(filename=filename, dir=dir)
        par = _OSPar.from_data(response['download_par'])
        par.read(privkey).get_object_as_file(filename)
        par.close(privkey)
        filemeta.assert_correct_data(filename=filename)
        if filemeta.is_compressed():
            from Acquire.Client import uncompress as _uncompress
            _uncompress(inputfile=filename, outputfile=filename, compression_type=filemeta.compression_type())
    elif ('downloader' in response):
        from Acquire.Client import ChunkDownloader as _ChunkDownloader
        downloader = _ChunkDownloader.from_data(response['downloader'], privkey=privkey, service=storage_service)
        filename = downloader.download(filename=filename, dir=dir)
    filemeta._copy_credentials(self._metadata)
    self._metadata = filemeta
    return filename
