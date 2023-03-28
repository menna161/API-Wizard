from __future__ import print_function, unicode_literals, division, absolute_import
import os, sys, json, subprocess, tempfile, multiprocessing
import datetime
import gzip
import hashlib
import io
import tarfile
import stat
import dxpy
import dxpy.executable_builder
from . import logger
from .utils import merge
from .utils.printing import fill
from .compat import input
from .cli import INTERACTIVE_CLI


def upload_applet(src_dir, uploaded_resources, check_name_collisions=True, overwrite=False, archive=False, project=None, override_folder=None, override_name=None, dry_run=False, brief=False, **kwargs):
    '\n    Creates a new applet object.\n\n    :param project: ID of container in which to create the applet.\n    :type project: str, or None to use whatever is specified in dxapp.json\n    :param override_folder: folder name for the resulting applet which, if specified, overrides that given in dxapp.json\n    :type override_folder: str\n    :param override_name: name for the resulting applet which, if specified, overrides that given in dxapp.json\n    :type override_name: str\n\n    '
    applet_spec = _get_applet_spec(src_dir)
    if (project is None):
        dest_project = applet_spec['project']
    else:
        dest_project = project
        applet_spec['project'] = project
    if ('name' not in applet_spec):
        try:
            applet_spec['name'] = os.path.basename(os.path.abspath(src_dir))
        except:
            raise AppBuilderException(('Could not determine applet name from the specification (dxapp.json) or from the name of the working directory (%r)' % (src_dir,)))
    if override_folder:
        applet_spec['folder'] = override_folder
    if ('folder' not in applet_spec):
        applet_spec['folder'] = '/'
    if override_name:
        applet_spec['name'] = override_name
    if ('dxapi' not in applet_spec):
        applet_spec['dxapi'] = dxpy.API_VERSION
    applets_to_overwrite = []
    archived_applet = None
    if (check_name_collisions and (not dry_run)):
        destination_path = ((applet_spec['folder'] + ('/' if (not applet_spec['folder'].endswith('/')) else '')) + applet_spec['name'])
        logger.debug(('Checking for existing applet at ' + destination_path))
        for result in dxpy.find_data_objects(classname='applet', name=applet_spec['name'], folder=applet_spec['folder'], project=dest_project, recurse=False):
            if overwrite:
                applets_to_overwrite.append(result['id'])
            elif archive:
                logger.debug(('Archiving applet %s' % result['id']))
                proj = dxpy.DXProject(dest_project)
                archive_folder = '/.Applet_archive'
                try:
                    proj.list_folder(archive_folder)
                except dxpy.DXAPIError:
                    proj.new_folder(archive_folder)
                proj.move(objects=[result['id']], destination=archive_folder)
                archived_applet = dxpy.DXApplet(result['id'], project=dest_project)
                now = datetime.datetime.fromtimestamp((archived_applet.created / 1000)).ctime()
                new_name = (archived_applet.name + ' ({d})'.format(d=now))
                archived_applet.rename(new_name)
                if (not brief):
                    logger.info(('Archived applet %s to %s:"%s/%s"' % (result['id'], dest_project, archive_folder, new_name)))
            else:
                raise AppBuilderException(('An applet already exists at %s (id %s) and the --overwrite (-f) or --archive (-a) options were not given' % (destination_path, result['id'])))
    applet_spec['runSpec'].setdefault('bundledDepends', [])
    applet_spec['runSpec'].setdefault('assetDepends', [])
    if (not dry_run):
        region = dxpy.api.project_describe(dest_project, input_params={'fields': {'region': True}})['region']
        if ((len(applet_spec.get('regionalOptions', {})) != 0) and (region not in applet_spec.get('regionalOptions', {}))):
            err_mesg = 'destination project is in region {} but "regionalOptions" do not contain this region. '.format(region)
            err_mesg += 'Please, update your "regionalOptions" specification'
            raise AppBuilderException(err_mesg)
        regional_options = applet_spec.get('regionalOptions', {}).get(region, {})
        if ('systemRequirements' in regional_options):
            applet_spec['runSpec']['systemRequirements'] = regional_options['systemRequirements']
        if ('bundledDepends' in regional_options):
            applet_spec['runSpec']['bundledDepends'].extend(regional_options['bundledDepends'])
        if ('assetDepends' in regional_options):
            applet_spec['runSpec']['assetDepends'].extend(regional_options['assetDepends'])
    dxpy.executable_builder.inline_documentation_files(applet_spec, src_dir)
    if ('file' in applet_spec['runSpec']):
        with open(os.path.join(src_dir, applet_spec['runSpec']['file'])) as code_fh:
            applet_spec['runSpec']['code'] = code_fh.read()
            del applet_spec['runSpec']['file']
    if ('systemRequirements' in applet_spec['runSpec']):
        sys_reqs = applet_spec['runSpec']['systemRequirements']
        for entry_point in sys_reqs:
            try:
                bootstrap_script = os.path.join(src_dir, sys_reqs[entry_point]['clusterSpec']['bootstrapScript'])
                with open(bootstrap_script) as code_fh:
                    sys_reqs[entry_point]['clusterSpec']['bootstrapScript'] = code_fh.read()
            except KeyError:
                continue
            except IOError:
                raise AppBuilderException('The clusterSpec "bootstrapScript" could not be read.')
    if (uploaded_resources is not None):
        applet_spec['runSpec']['bundledDepends'].extend(uploaded_resources)
    asset_depends = applet_spec['runSpec']['assetDepends']
    if ((type(asset_depends) is not list) or any(((type(dep) is not dict) for dep in asset_depends))):
        raise AppBuilderException('Expected runSpec.assetDepends to be an array of objects')
    for asset in asset_depends:
        asset_project = asset.get('project', None)
        asset_folder = asset.get('folder', '/')
        asset_stages = asset.get('stages', None)
        if ('id' in asset):
            asset_record = dxpy.DXRecord(asset['id']).describe(fields={'details'}, default_fields=True)
        elif (('name' in asset) and (asset_project is not None) and ('version' in asset)):
            try:
                asset_record = dxpy.find_one_data_object(zero_ok=True, classname='record', typename='AssetBundle', name=asset['name'], properties=dict(version=asset['version']), project=asset_project, folder=asset_folder, recurse=False, describe={'defaultFields': True, 'fields': {'details': True}}, state='closed', more_ok=False)
            except dxpy.exceptions.DXSearchError:
                msg = 'Found more than one asset record that matches: name={0}, folder={1} in project={2}.'
                raise AppBuilderException(msg.format(asset['name'], asset_folder, asset_project))
        else:
            raise AppBuilderException("Each runSpec.assetDepends element must have either {'id'} or {'name', 'project' and 'version'} field(s).")
        if asset_record:
            if ('id' in asset):
                asset_details = asset_record['details']
            else:
                asset_details = asset_record['describe']['details']
            if ('archiveFileId' in asset_details):
                archive_file_id = asset_details['archiveFileId']
            else:
                raise AppBuilderException(("The required field 'archiveFileId' was not found in the details of the asset bundle %s " % asset_record['id']))
            archive_file_name = dxpy.DXFile(archive_file_id).describe()['name']
            bundle_depends = {'name': archive_file_name, 'id': archive_file_id}
            if asset_stages:
                bundle_depends['stages'] = asset_stages
            applet_spec['runSpec']['bundledDepends'].append(bundle_depends)
            if ((not dry_run) and (dxpy.DXRecord(dxid=asset_record['id'], project=dest_project).describe()['project'] != dest_project)):
                dxpy.DXRecord(asset_record['id'], project=asset_record['project']).clone(dest_project)
        else:
            raise AppBuilderException(('No asset bundle was found that matched the specification %s' % json.dumps(asset)))
    merge(applet_spec, kwargs)
    if dry_run:
        print('Would create the following applet:')
        print(json.dumps(applet_spec, indent=2))
        print('*** DRY-RUN-- no applet was created ***')
        return (None, None)
    if applet_spec.get('categories', []):
        if ('tags' not in applet_spec):
            applet_spec['tags'] = []
        applet_spec['tags'] = list((set(applet_spec['tags']) | set(applet_spec['categories'])))
    applet_id = dxpy.api.applet_new(applet_spec)['id']
    if archived_applet:
        archived_applet.set_properties({'replacedWith': applet_id})
    if applets_to_overwrite:
        if (not brief):
            logger.info(('Deleting applet(s) %s' % ','.join(applets_to_overwrite)))
        dxpy.DXProject(dest_project).remove_objects(applets_to_overwrite)
    return (applet_id, applet_spec)
