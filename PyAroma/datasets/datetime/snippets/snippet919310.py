from db.database import close, _get_remind
import datetime
from utils.constants import DATETIME_FORMAT


def close_remind_button(bot, chat_id):
    try:
        closed_id = close(chat_id, '')
        for r in _get_remind(chat_id, closed_id):
            remind = f"""⏰ Remind ({r['id']}): 📌 "{r['remind_text']} on {datetime.datetime.strptime(r['remind_time'], DATETIME_FORMAT).strftime('%d.%m %H:%M')}" marked as Done!✅"""
        bot.send_message(chat_id=chat_id, text=remind)
    except:
        bot.send_message(chat_id=chat_id, text='Sorry, there is no remind(s) with such id(s) 😔')
