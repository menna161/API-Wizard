import datetime


def add_user(self, name, amount, email=None):
    name = (name[0].upper() + name[1:].lower())
    amount = ('%.2f' % amount)
    detail = {'name': name, 'amount': amount}
    today = datetime.date.today()
    date_text = '{today.month}/{today.day}/{today.year}'.format(today=today)
    detail['date'] = date_text
    if (email is not None):
        detail['email'] = email
    self.user_details.append(detail)
