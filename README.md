# API Wizard IDE Plugin
This repositry includes our source code work for our thesis project at The American University in Cairo 
Supervised by Dr.Sarah Nadi (nadi@ualberta.ca) and Dr.Ahmead Rafea (rafea@aucegypt.edu)

# Overview
API Wizard is a VSCode IDE plugin based on pattern mining that allows users to view a common usage example of a certain Python API they would like to use.
Using this plugin, you can easily use a keyboard shortcut over the API query to invoke the IDE plugin which views the usage example of this API. This project reimplements the algorithm of the state-of-the-art tool Exempla Gratis with some modifications to overcome the limitations discussed in our paper.
API Wizard uses Gspan as its mining frequent subgraphs algorithm.

These are the 6 main milestones of API-Wizrd. API Wizard takes a set of filtered code snippets, each code snippet is represented by an AST tree. Then we find the common patterns between the different AST trees using the Gspan tool. The Gspan is a pattern mining tool that outputs patterns that exists in 50% of the trees. So, Next we  remove the subtrees that exists in larger tress. So, We only consider the maximal frequent subtree. The maximal frequent subtrees forms an  incomplete code template with placeholders that needs to be filled to finally generate a complete code example.

![image](https://github.com/menna161/API-Wizard/assets/57011308/115feaf1-82dc-49e4-a412-da3a83014bc2)


In this API-Wizard folder, you can find the source code for API-Wizard. The subfiles are numbered according to the function corresponding milestone. There is also the helper folder that contains the functions used throughout the project in different milestones. The evaluation folder has the code for calculating some of our evaluation metrics: conciseness and representativeness. API_WIzard.py is the file that contains the main function for the tool. The dataset folder holds all the dataset we have tested our tool with. PyAroma folders holds the source code of our re-implemetation of Aroma. The folder dataset_extraction_code has the scripts used to extract our dataset.


# Getting Started
In order ti use the IDE plugin, install the API Wizard extension in vscode through this link https://marketplace.visualstudio.com/items?itemName=API-Wizard.API-Wizard and use it as instructed. 

Steps to run API-Wizard using command line:

first, there are some packaes you need to install before running our tool. To install them use these commands in the project folder:
- pip install gspan-mining
- pip install astor
- cd .\API-Wizard\
- cd .\API-Wizard\
- python .\API_WIzard.py

To use the plugin you need Visula Studio Code and then to use the extension you follow the steps in this link https://code.visualstudio.com/api/get-started/your-first-extension 
Then you need to replace the code in the package.js with the code in this reposity under the same name. Then in order to test it, open a python file in vscode and write a python API and then run the extension using ctrs+shift+P and then choose API Wizard from the drop down menu. 


Steps to run PyAroma:
- cd PyAroma/reference/evaluation/
- ./run_all
The results are expected to be found in the file called "aroma_results.csv" inside the "reference" directory. Note that new results are appended to the end of this file.

# Usage
Type the name of the API you want an example for. Then, Initiate the plugin using the keyboard shortcut (ctrl+alt+w)

# Contributing
Contributions are welcome and encouraged! To contribute to API Wizard, follow these steps:
- Fork the repository.
- Create a new branch for your changes.
- Make your changes and commit them.
- Push your changes to your forked repository.
- Submit a pull request.


# License
API Wizard is licensed under the MIT license. See LICENSE for more information.

# Contact
If you have any questions or concerns about API Wizard, please contact us at
1.	mennatag@aucrgypt.edu
2.	mariamdaabis@aucegypt.edu
3.	dinabishr@aucegypt.edu
4.	mennaelzahar@aucegypt.edu
5.	nehalfooda@aucegypt.edu
6.	nadatamer@aucegypt.edu


Thank you for using API Wizard!
