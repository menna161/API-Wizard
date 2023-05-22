import datetime


def make_messages(names, amounts):
    messages = []
    if (len(names) == len(amounts)):
        i = 0
        today = datetime.date.today()
        text = '{today.month}/{today.day}/{today.year}'.format(today=today)
        for name in names:
            "\n            Here's a simple solution to capitalize \n            everyone's name prior to sending\n            "
            name = (name[0].upper() + name[1:].lower())
            '\n            Did you get the bonus??\n            '
            new_amount = ('%.2f' % amounts[i])
            new_msg = unf_message.format(name=name, date=text, total=new_amount)
            i += 1
            print(new_msg)
