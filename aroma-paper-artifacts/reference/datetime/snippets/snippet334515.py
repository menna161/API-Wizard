from google.apputils import basetest
from googleapis.codegen.java_import_manager import JavaImportManager


def testAddImportConflictingNames(self):
    datetime1_import = 'com.google.api.client.util.DateTime'
    datetime2_import = 'com.test.testing.util.DateTime'
    self.assertTrue(self.import_manager.AddImport(datetime1_import))
    self.assertFalse(self.import_manager.AddImport(datetime2_import))
    self.assertEquals(datetime1_import, self.import_manager._class_name_to_qualified_name['DateTime'])
