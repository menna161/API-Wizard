import json
import os
import random
import time
import traceback
import requests
import requests.utils
from . import config, devices


def login_flow(self, just_logged_in=False, app_refresh_interval=1800):
    self.last_experiments = time.time()
    self.logger.info('LOGIN FLOW! Just logged-in: {}'.format(just_logged_in))
    check_flow = []
    if just_logged_in:
        try:
            check_flow.append(self.sync_launcher(False))
            check_flow.append(self.get_account_family())
            check_flow.append(self.get_zr_token_result())
            check_flow.append(self.sync_device_features(False))
            check_flow.append(self.banyan())
            check_flow.append(self.creatives_ar_class())
            check_flow.append(self.get_reels_tray_feed(reason='cold_start'))
            check_flow.append(self.get_timeline_feed())
            check_flow.append(self.push_register())
            check_flow.append(self.media_blocked())
            check_flow.append(self.get_loom_fetch_config())
            check_flow.append(self.get_news_inbox())
            check_flow.append(self.get_business_branded_content())
            check_flow.append(self.get_scores_bootstrap())
            check_flow.append(self.get_monetization_products_eligibility_data())
            check_flow.append(self.get_linked_accounts())
            check_flow.append(self.get_cooldowns())
            check_flow.append(self.push_register())
            check_flow.append(self.arlink_download_info())
            check_flow.append(self.get_username_info(self.user_id))
            check_flow.append(self.get_presence())
            check_flow.append(self.get_direct_v2_inbox2())
            check_flow.append(self.topical_explore())
            check_flow.append(self.get_direct_v2_inbox())
            check_flow.append(self.notification_badge())
            check_flow.append(self.facebook_ota())
        except Exception as e:
            self.logger.error('Exception raised: {}\n{}'.format(e, traceback.format_exc()))
            return False
    else:
        try:
            pull_to_refresh = ((random.randint(1, 100) % 2) == 0)
            check_flow.append(self.get_timeline_feed(options=(['is_pull_to_refresh'] if (pull_to_refresh is True) else [])))
            check_flow.append(self.get_reels_tray_feed(reason=('pull_to_refresh' if (pull_to_refresh is True) else 'cold_start')))
            is_session_expired = ((time.time() - self.last_login) > app_refresh_interval)
            if is_session_expired:
                self.last_login = time.time()
                self.client_session_id = self.generate_UUID(uuid_type=True)
                check_flow.append(self.get_ranked_recipients('reshare', True))
                check_flow.append(self.get_ranked_recipients('save', True))
                check_flow.append(self.get_inbox_v2())
                check_flow.append(self.get_presence())
                check_flow.append(self.get_recent_activity())
                check_flow.append(self.get_profile_notice())
                check_flow.append(self.explore(False))
            if ((time.time() - self.last_experiments) > 7200):
                check_flow.append(self.sync_device_features())
        except Exception as e:
            self.logger.error('Error loginin, exception raised: {}\n{}'.format(e, traceback.format_exc()))
            return False
    self.save_uuid_and_cookie()
    return (False if (False in check_flow) else True)
