"""# Input Code Snippet"""

import os


def read_dir(api_name):

    pdir_path = '/Users/nehalfooda/Downloads/Thesis/API/'
    # The API name from the user
    api_file_name = 'MinMaxScaler'
    dir_path = pdir_path + api_name
    ex = []
    # count = 0
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.py'):
            with open(os.path.join(dir_path, file_name), 'r') as file:
                text = file.read()
                ex.append(text)
                # count += 1  # Increment the counter
                # if count >= 100:  # Check if the counter has reached 100
                #     break

    print('read files: ', len(ex))
    return ex
