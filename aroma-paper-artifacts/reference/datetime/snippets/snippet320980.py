import logging
import os
from aminator.config import init_defaults, configure_datetime_logfile
from aminator.environment import Environment
from aminator.plugins import PluginManager
from aminator.util.linux import mkdir_p


def __init__(self, config=None, parser=None, plugin_manager=PluginManager, environment=Environment, debug=False, envname=None):
    log.info('Aminator starting...')
    if (not all((config, parser))):
        log.debug('Loading default configuration')
        (config, parser) = init_defaults(debug=debug)
    self.config = config
    self.parser = parser
    log.debug('Configuration loaded')
    if (not envname):
        envname = self.config.environments.default
    self.plugin_manager = plugin_manager(self.config, self.parser, plugins=self.config.environments[envname])
    log.debug('Plugins loaded')
    self.parser.parse_args()
    log.debug('Args parsed')
    os.environ['AMINATOR_PACKAGE'] = self.config.context.package.arg
    log.debug('Creating initial folder structure if needed')
    mkdir_p(self.config.log_root)
    mkdir_p(os.path.join(self.config.aminator_root, self.config.lock_dir))
    mkdir_p(os.path.join(self.config.aminator_root, self.config.volume_dir))
    if self.config.logging.aminator.enabled:
        log.debug('Configuring per-package logging')
        configure_datetime_logfile(self.config, 'aminator')
    self.environment = environment()
