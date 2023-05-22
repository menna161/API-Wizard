from db.database import get_reminds
from datetime import datetime
from utils.constants import DATETIME_FORMAT, LIST_ALL_FLAG, LIST_WEEK_FLAG, LIST_ALL_BUTTON, LIST_WEEK_BUTTON, LIST_10_BUTTON, LIST_30_BUTTON
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.menu import build_menu


def button_list_reminds(bot, user_chat_id, args):
    my_reminds = ''
    remind_status = ''
    interval = ''.join(args).lower()
    try:
        for r in get_reminds(user_chat_id, interval):
            if (r['expired'] == False):
                remind_status = '🕖'
            elif (r['expired'] == True):
                remind_status = '❌'
            if (r['done'] == True):
                remind_status = '✅'
            time = datetime.strptime(r['remind_time'], DATETIME_FORMAT).strftime('%d.%m %H:%M')
            my_reminds += f'''🗓 {r['id']}: ⏰ {time} 📌 {r['remind_text']}: {remind_status}
'''
        bot.send_message(chat_id=user_chat_id, text=my_reminds)
        list_button_menu(bot, user_chat_id)
    except:
        if (interval == ''):
            interval = 'today'
        my_reminds = f'Oops 😯, you have no reminds for {interval}.'
        bot.send_message(chat_id=user_chat_id, text=my_reminds)
