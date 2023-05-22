from io import StringIO
import glob
import grt
import mforms
import datetime
from wb import DefineModule, wbinputs
from workbench.ui import WizardForm, WizardPage
from mforms import newButton, newCodeEditor, FileChooser


def save_clicked(self):
    file_chooser = mforms.newFileChooser(self.main, mforms.OpenDirectory)
    if (file_chooser.run_modal() == mforms.ResultOk):
        path = file_chooser.get_path()
        i = len(glob.glob((path + '/*_table.php')))
        now = datetime.datetime.now()
        for key in sorted(migrations):
            try:
                search_format = '*_create_{tableName}_table.php'.format(tableName=migration_tables[key])
                search = glob.glob(((path + '/') + search_format))
                for file in search:
                    with open(file, 'w+') as f:
                        f.write(''.join(migrations[key]))
                if (len(search) == 0):
                    save_format = '{year}_{month}_{day}_{number}_create_{tableName}_table.php'.format(year=now.strftime('%Y'), month=now.strftime('%m'), day=now.strftime('%d'), number=str(i).zfill(6), tableName=migration_tables[key])
                    with open(((path + '/') + save_format), 'w+') as f:
                        f.write(''.join(migrations[key]))
                        i += 1
            except IOError as e:
                mforms.Utilities.show_error('Save to File', ('Could not save to file "%s": %s' % (path, str(e))), 'OK', '', '')
