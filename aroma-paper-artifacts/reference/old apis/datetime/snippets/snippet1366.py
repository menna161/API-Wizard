import csv
import datetime
import shutil
from tempfile import NamedTemporaryFile


def append_data(file_path, name, email, amount):
    fieldnames = ['id', 'name', 'email', 'amount', 'sent', 'date']
    next_id = get_length(file_path)
    with open(file_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'id': next_id, 'name': name, 'email': email, 'sent': '', 'amount': amount, 'date': datetime.datetime.now()})
