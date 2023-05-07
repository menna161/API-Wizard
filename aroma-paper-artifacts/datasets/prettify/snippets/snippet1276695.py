import errno
import io
import os
import shutil
import tempfile
from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
from notebook.services.config import ConfigManager as FrontendConfigManager
from traitlets.config import Config
from traitlets.config.manager import BaseJSONConfigManager
from jupyter_contrib_nbextensions.install import _set_managed_config, _update_config_list
import logging
import pip


def _migrate_require_paths(logger=None):
    'Migrate require paths from old to new values.'
    if logger:
        logger.info('- Migrating require paths from old to new locations')
    mappings = {'notebook': ([('config/config_menu/main', 'nbextensions_configurator/config_menu/main'), ('skill/skill', 'skill/main'), ('yapf_ext/yapf_ext', 'code_prettify/code_prettify')] + [(req, req.split('/', 1)[1]) for req in ['codemirrormode/skill/skill', 'publishing/gist_it/main', 'publishing/printview/main', 'styling/table_beautifier/main', 'styling/zenmode/main', 'usability/autosavetime/main', 'usability/autoscroll/main', 'usability/chrome-clipboard/main', 'usability/code_font_size/code_font_size', 'usability/codefolding/main', 'usability/collapsible_headings/main', 'usability/comment-uncomment/main', 'usability/datestamper/main', 'usability/dragdrop/main', 'usability/equation-numbering/main', 'usability/execute_time/ExecuteTime', 'usability/exercise/main', 'usability/exercise2/main', 'usability/freeze/main', 'usability/help_panel/help_panel', 'usability/hide_input/main', 'usability/hide_input_all/main', 'usability/highlighter/highlighter', 'usability/hinterland/hinterland', 'usability/init_cell/main', 'usability/keyboard_shortcut_editor/main', 'usability/latex_envs/latex_envs', 'usability/limit_output/main', 'usability/move_selected_cells/main', 'usability/navigation-hotkeys/main', 'usability/notify/notify', 'usability/python-markdown/main', 'usability/qtconsole/qtconsole', 'usability/rubberband/main', 'usability/ruler/main', 'usability/runtools/main', 'usability/scratchpad/main', 'usability/search-replace/main', 'usability/skip-traceback/main', 'usability/spellchecker/main', 'usability/splitcell/splitcell', 'usability/toc2/main', 'usability/toggle_all_line_numbers/main']]), 'tree': [('usability/tree-filter/index', 'tree-filter/index')]}
    fecm = FrontendConfigManager()
    for section in mappings:
        conf = fecm.get(section)
        load_extensions = conf.get('load_extensions', {})
        for (old, new) in mappings[section]:
            status = load_extensions.pop(old, None)
            if (status is not None):
                if logger:
                    logger.debug('--  Migrating {!r} -> {!r}'.format(old, new))
                load_extensions[new] = status
        fecm.set(section, conf)
