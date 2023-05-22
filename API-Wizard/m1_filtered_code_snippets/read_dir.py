import os
import pandas as pd


#Function to read the snippets that conatins the api_name given as input
#Returns the list of read code snippets

def read_dir(api_name):
    # Define the directory path where the files are located
    dir_path = '../Test_Data/'

    # Append the specified API name to the directory path
    dir_path = dir_path + api_name

    # Create an empty list to store the file contents
    ex = []

    # Iterate over each file in the directory
    for file_name in os.listdir(dir_path):
        # Check if the file ends with '.py' extension
        if file_name.endswith('.py'):
            # Open the file in read mode
            with open(os.path.join(dir_path, file_name), 'r') as file:
                # Read the contents of the file
                text = file.read()
                # Append the file contents to the 'ex' list
                ex.append(text)
    
    print('Read Files Succesfully')
    
    # Return the list of file contents
    return ex
