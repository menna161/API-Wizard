from datetime import datetime
import message


def parse(self):
    list_of_messages = []
    set_of_senders = set()
    for l in self.raw_messages:
        content = l['message'].encode('utf-8')
        sender = l['from'].encode('utf-8')
        datetime_str = l['datetime'].encode('utf-8')
        (date, time) = datetime_str.split('T')
        time = time.replace('+0000', '')
        msg_date = ((date + ' ') + time)
        datetime_obj = datetime.strptime(msg_date, '%Y-%m-%d %H:%M:%S')
        set_of_senders.add(sender)
        list_of_messages.append(message.Message(sender, content, date, time, datetime_obj))
    return (list(set_of_senders), list_of_messages)
