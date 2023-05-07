from tqdm import tqdm
from datetime import timedelta


def comment(self, media_id, comment_text):
    if self.is_commented(media_id):
        return True
    if (not self.reached_limit('comments')):
        if self.blocked_actions['comments']:
            self.logger.warning('YOUR `COMMENT` ACTION IS BLOCKED')
            if self.blocked_actions_protection:
                from datetime import timedelta
                next_reset = (self.start_time.date() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                self.logger.warning('blocked_actions_protection ACTIVE. Skipping `comment` action till, at least, {}.'.format(next_reset))
                return False
        self.delay('comment')
        _r = self.api.comment(media_id, comment_text)
        if (_r == 'feedback_required'):
            self.logger.error('`Comment` action has been BLOCKED...!!!')
            return False
        if _r:
            self.total['comments'] += 1
            return True
    else:
        self.logger.info('Out of comments for today.')
    return False
