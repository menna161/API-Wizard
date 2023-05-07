import json
from datetime import datetime
import pandas as pd
from seodeploy.lib.modules import ModuleConfig
from seodeploy.lib.logging import get_logger
from seodeploy.lib.config import Config


def execute(self, sample_paths=None):
    'Execute modules against argument, sample_paths.'
    self.summary = {'started': str(datetime.now())}
    self.sample_paths = (sample_paths or self.sample_paths)
    self.summary.update({'samples': len(self.sample_paths)})
    self.modules = self.module_config.module_names
    self.summary.update({'modules': ','.join(self.modules)})
    print()
    print('SEODeploy: Brought to you by LOCOMOTIVE®')
    print('Loaded...')
    print()
    for active_module in self.module_config.active_modules:
        module_config = Config(module=active_module, cfiles=self.config.cfiles[:1])
        module = self.module_config.active_modules[active_module].SEOTestingModule(config=module_config)
        print('Running Module: {}'.format(module.modulename))
        _LOG.info('Running Module: {}'.format(module.modulename))
        (messages, errors) = module.run(sample_paths=self.sample_paths)
        print('Number of Messages: {}'.format(len(messages)))
        _LOG.info('Number of Messages: {}'.format(len(messages)))
        passing = (len(messages) == 0)
        self._update_messages(messages)
        self._update_passing(passing)
        self.summary.update({'{} passing: '.format(module.modulename): passing})
        self.summary.update({'{} errors: '.format(module.modulename): len(errors)})
        if errors:
            _LOG.error(('Run Errors:' + json.dumps(errors, indent=2)))
        print()
    self.get_messages().to_csv('output.csv', index=False)
    self.print_summary()
    return self.passing
