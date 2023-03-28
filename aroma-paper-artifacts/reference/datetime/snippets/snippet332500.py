import os
import subprocess
import platform
import datetime
import socket
from ansible.module_utils.basic import *


def main(self):
    state = self.module.params['state']
    src = self.module.params['src']
    dest = self.module.params['dest']
    logdir = self.module.params['logdir']
    accessRights = self.module.params['accessRights']
    dest = os.path.expanduser(dest)
    if (state == 'present'):
        if self.module.check_mode:
            self.module.exit_json(changed=False, msg='IBM IM where to be installed at {0}'.format(dest))
        if (not self.isProvisioned(dest)):
            if (not os.path.exists((src + '/install'))):
                self.module.fail_json(msg=(src + '/install not found'))
            if (not os.path.exists(logdir)):
                if (not os.listdir(logdir)):
                    os.makedirs(logdir)
            logfile = '{0}_ibmim_{1}.xml'.format(platform.node(), datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
            installCmd = '{0}/tools/imcl install com.ibm.cic.agent -repositories {0}/repository.config -accessRights {1} -acceptLicense -log {2}/{3} -installationDirectory {4} -properties com.ibm.cic.common.core.preferences.preserveDownloadedArtifacts=true'.format(src, accessRights, logdir, logfile, dest)
            print(("installCmd is: '%s'" % installCmd))
            child = subprocess.Popen([installCmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout_value, stderr_value) = child.communicate()
            stdout_value = repr(stdout_value)
            stderr_value = repr(stderr_value)
            if (child.returncode != 0):
                self.module.fail_json(msg='IBM IM installation failed', stderr=stderr_value, stdout=stdout_value, module_facts=self.module_facts)
            self.getVersion(dest)
            self.module.exit_json(msg='IBM IM installed successfully', changed=True, stdout=stdout_value, stderr=stderr_value, module_facts=self.module_facts)
        else:
            self.module.exit_json(changed=False, msg='IBM IM is already installed', module_facts=self.module_facts)
    if (state == 'absent'):
        if self.module.check_mode:
            self.module.exit_json(changed=False, msg='IBM IM where to be uninstalled from {0}'.format(dest), module_facts=self.module_facts)
        if self.isProvisioned(dest):
            if (accessRights == 'admin'):
                uninstall_dir = '/var/ibm/InstallationManager/uninstall/uninstallc'
            else:
                uninstall_dir = os.path.expanduser('~/var/ibm/InstallationManager/uninstall/uninstallc')
            if (not os.path.exists(uninstall_dir)):
                self.module.fail_json(msg=(uninstall_dir + ' does not exist'))
            child = subprocess.Popen([uninstall_dir], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout_value, stderr_value) = child.communicate()
            stdout_value = repr(stdout_value)
            stderr_value = repr(stderr_value)
            if (child.returncode != 0):
                self.module.fail_json(msg='IBM IM uninstall failed', stderr=stderr_value, stdout=stdout_value, module_facts=self.module_facts)
            self.module.exit_json(changed=True, msg='IBM IM uninstalled successfully', stdout=stdout_value, module_facts=self.module_facts)
        else:
            self.module.exit_json(changed=False, msg='IBM IM is not installed', module_facts=self.module_facts)
