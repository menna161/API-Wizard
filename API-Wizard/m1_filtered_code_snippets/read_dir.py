# from google.colab import drive
import os
import pandas as pd


def read_dir(api_name):
    
    # drive.mount('/content/gdrive')
    # dir_path = '/content/gdrive/Shareddrives/Thesis 2/our data/'
    # dir_path = '/Users/nehalfooda/Downloads/Thesis/IDE/'
    dir_path = '../Test_Data/'

    dir_path = dir_path + api_name

    ex = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.py'):
            with open(os.path.join(dir_path, file_name), 'r') as file:
                text = file.read()
                ex.append(text)
               
    
    print('Read Files Succesfully: ', len(ex))
    return ex