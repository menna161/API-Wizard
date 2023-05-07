from datetime import datetime
import pytz
from seodeploy.lib.modules import ModuleBase
from seodeploy.lib.config import Config
from seodeploy.modules.contentking.functions import run_contentking, load_report
from seodeploy.modules.contentking.exceptions import ContentSamplingError


def run(self, sample_paths=None):
    'Run the ContentKing Module.'
    start_time = datetime.now().astimezone(self.time_zone)
    self.sample_paths = (sample_paths or self.sample_paths)
    page_data = run_contentking(sample_paths, start_time, self.time_zone, self.config)
    (diffs, errors) = self.run_diffs(page_data)
    self.messages = self.prepare_messages(diffs)
    return (self.messages, errors)
