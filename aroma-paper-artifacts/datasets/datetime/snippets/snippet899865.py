import os
import webbrowser
import datetime
import py_cui.widget_set
import pyautogit
import pyautogit.screen_manager
import pyautogit.logger as LOGGER
import urllib.request
import urllib.error


def initialize_screen_elements(self):
    'Override of base class function. Initializes widgets, and returns widget set\n\n        Returns\n        -------\n        settings_widget_set : py_cui.widget_set.WidgetSet\n            Widget set object for rsettings screen\n        '
    settings_widget_set = self.manager.root.create_new_widget_set(9, 6)
    settings_widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.manager.open_repo_select_window)
    logo_label = settings_widget_set.add_block_label(self.get_settings_ascii_art(), 0, 0, row_span=2, column_span=3, center=True)
    logo_label.set_color(py_cui.RED_ON_BLACK)
    link_label = settings_widget_set.add_label('Settings Screen - pyautogit v{}'.format(pyautogit.__version__), 0, 3, row_span=2, column_span=3)
    link_label.add_text_color_rule('Settings Screen*', py_cui.CYAN_ON_BLACK, 'startswith', match_type='line')
    debug_log_label = settings_widget_set.add_label('Debug Logging', 2, 0)
    debug_log_label.toggle_border()
    self.debug_log_toggle = settings_widget_set.add_button('Toggle Logs', 2, 1, command=self.toggle_logging)
    self.debug_enter_path_button = settings_widget_set.add_button('Set Log File', 2, 2, command=self.ask_log_file_path)
    self.debug_log_status_label = settings_widget_set.add_label('OFF - {}'.format(LOGGER._LOG_FILE_PATH), 3, 0, column_span=3)
    editor_label = settings_widget_set.add_label('Default Editor', 4, 0)
    editor_label.toggle_border()
    self.external_editor_toggle = settings_widget_set.add_button('External/Internal', 4, 1, command=self.toggle_editor_type)
    self.external_editor_enter = settings_widget_set.add_button('Select Editor', 4, 2, command=self.ask_default_editor)
    self.editor_status_label = settings_widget_set.add_label('{} - {}'.format(self.manager.editor_type, self.manager.default_editor), 5, 0, column_span=3)
    about_label = settings_widget_set.add_label('About', 6, 0)
    about_label.toggle_border()
    self.fetch_readme_file_button = settings_widget_set.add_button('README', 6, 1, command=(lambda : self.fetch_about_file('README.md')))
    self.fetch_authors_button = settings_widget_set.add_button('Authors', 6, 2, command=(lambda : self.fetch_about_file('AUTHORS')))
    self.fetch_license_button = settings_widget_set.add_button('License', 7, 1, command=(lambda : self.fetch_about_file('LICENSE')))
    self.revert_settings_log_button = settings_widget_set.add_button('Settings Log', 7, 2, command=self.revert_settings_log)
    docs_label = settings_widget_set.add_label('Docs', 8, 0)
    docs_label.toggle_border()
    self.show_tutorial_button = settings_widget_set.add_button('Tutorial', 8, 1, command=self.show_tutorial)
    self.open_web_docs_button = settings_widget_set.add_button('Online Docs', 8, 2, command=self.open_web_docs)
    self.settings_info_panel = settings_widget_set.add_text_block('Settings Info Log', 2, 3, row_span=7, column_span=3)
    self.settings_info_panel.set_selectable(False)
    self.info_panel = self.settings_info_panel
    if (not LOGGER._LOG_ENABLED):
        self.update_log_file_path('.pyautogit/{}.log'.format(str(datetime.datetime.today()).split(' ')[0]), default_path=True)
    return settings_widget_set
