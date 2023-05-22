from tqdm import tqdm
import time
from datetime import timedelta


def like_comment(self, comment_id):
    if (not self.reached_limit('likes')):
        if self.blocked_actions['likes']:
            self.logger.warning('YOUR `LIKE` ACTION IS BLOCKED')
            if self.blocked_actions_protection:
                from datetime import timedelta
                next_reset = (self.start_time.date() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                self.logger.warning('blocked_actions_protection ACTIVE. Skipping `like` action till, at least, {}.'.format(next_reset))
                return False
        self.delay('like')
        _r = self.api.like_comment(comment_id)
        if (_r == 'feedback_required'):
            self.logger.error('`Like` action has been BLOCKED...!!!')
            self.blocked_actions['likes'] = True
            return False
        if _r:
            self.logger.info('Liked comment {}.'.format(comment_id))
            self.total['likes'] += 1
            return True
    else:
        self.logger.info('Out of likes for today.')
    return False
