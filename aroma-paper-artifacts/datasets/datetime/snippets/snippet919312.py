from db.database import create
import datetime


def create_today(bot, update, args):
    try:
        user_chat_id = update.message.chat_id
        user_message = ' '.join(args).split(' ', 1)
        tomorrow_date = datetime.date.today().strftime('%Y-%d-%m')
        remind_full_time = ((tomorrow_date + ' ') + user_message[0])
        remind_text = user_message[1]
        remind = f'Remind 📌 "{remind_text}" scheduled for {user_message[0]} today 📆'
        create(user_chat_id, remind_full_time, remind_text, False)
        bot.send_message(chat_id=user_chat_id, text=remind)
    except IndexError:
        bot.send_message(chat_id=user_chat_id, text="Oops 😯, can't create remind. Maybe text is missing? 🤔")
    except ValueError:
        bot.send_message(chat_id=user_chat_id, text="Oops 😯, can't create remind. Maybe something wrong with time? 🤔")
    except:
        bot.send_message(chat_id=user_chat_id, text='Looks like you are trying to set remind to past date 🤔. Are you sure?')
