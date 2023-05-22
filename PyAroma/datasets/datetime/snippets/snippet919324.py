from db.database import _update_time, _get_last_remind
from datetime import datetime, timedelta
from utils.constants import DATETIME_FORMAT, HOUR


def postpone_1h(bot, user_chat_id):
    postpone_timedelta = '1'
    postpone_time = 0
    try:
        postpone_format = 'h'
        if (postpone_format.lower() == 'h'):
            postpone_time = (int(postpone_timedelta) * HOUR)
        elif (postpone_format.lower() == 'm'):
            postpone_time = int(postpone_timedelta)
        remind_id = _get_last_remind(user_chat_id)['id']
        old_time = _get_last_remind(user_chat_id)['remind_time']
        new_time = (datetime.strptime(old_time, DATETIME_FORMAT) + timedelta(minutes=postpone_time)).strftime(DATETIME_FORMAT)
        _update_time(user_chat_id, remind_id, new_time)
        bot.send_message(chat_id=user_chat_id, text=f'📌 Remind postponed for {str(timedelta(minutes=postpone_time))}')
    except ValueError:
        bot.send_message(chat_id=user_chat_id, text=f'Oops 😯, you forgot to specify postpone time!')
    except TypeError:
        bot.send_message(chat_id=user_chat_id, text=f'Sorry, there is no active remind to postpone😔')
