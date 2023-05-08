import csv
import pickle


def append_list_to_csv(filename, data_list):
    with open(filename, 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(data_list)


def read_csv(filename):

    with open(filename, 'r') as file_read:
        reader = csv.reader(file_read)

        for row in reader:
            funcs = row[0]  # Assuming the first column is the key
            funcs = funcs.replace(" ", "")
            func_list = funcs.split(",")
            for i in range(1, len(func_list)):
                tmp_list = func_list[i].split(".")
                func_list[i] = tmp_list[-1]

            append_list_to_csv(filename_write, func_list)


def read_csv_to_dict(filename):
    data_dict = {}

    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            key = row[0]  # Assuming the first column is the key
            values = row[1:]  # Assuming the remaining columns are the values

            data_dict[key] = values

    return data_dict


def save_dict(filename, dict):
    with open(filename, 'wb') as fp:
        pickle.dump(dict, fp)


# Replace with the actual filename
filename_read = 'suggested_relevant_functions.csv'
filename_write = 'relevant_functions.csv'
filename_dict = 'relevant_functions.pkl'

# function calls

# read_csv(filename_read)
# dict = read_csv_to_dict(filename_write)
# save_dict(filename_dict, dict)


# test
# with open(filename_dict, 'rb') as fp:
#     dict = pickle.load(fp)
#     print(dict['value_counts'])
