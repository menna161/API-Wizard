import datetime
import os


def save_user_stats(self, username, path=''):
    if (not username):
        username = self.api.username
    user_id = self.convert_to_user_id(username)
    infodict = self.get_user_info(user_id, use_cache=False)
    if infodict:
        data_to_save = {'date': str(datetime.datetime.now().replace(microsecond=0)), 'followers': int(infodict['follower_count']), 'following': int(infodict['following_count']), 'medias': int(infodict['media_count'])}
        file_path = os.path.join(path, ('%s.tsv' % username))
        dump_data(data_to_save, file_path)
        self.logger.info(('Stats saved at %s.' % data_to_save['date']))
    return False
