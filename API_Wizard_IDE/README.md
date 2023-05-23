# api-wizrd README

API Wizard is a VSCode IDE plugin based on pattern mining that allows users to view a common usage example of a certain Python API they would like to use. Using this plugin, you can easily use a keyboard shortcut over the API query to invoke the IDE plugin which views the usage example of this API. This project reimplements the algorithm of the state-of-the-art tool Exempla Gratis with some modifications to overcome the limitations discussed in our paper. API Wizard uses Gspan as its mining frequent subgraphs algorithm.


## Requirements

You have to install some packages to run the IDE:

- pip install gspan-mining
- pip install astor
- Make sure you have Node.js installed

then run:

- npm install

## Known Issues

API Wizard can generate incomplete lines of code. The output lines can also be unordered.



### 1.0.0

Initial release of API Wizard



---

## Working with Markdown

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux)
* Toggle preview (`Shift+Cmd+V` on macOS or `Shift+Ctrl+V` on Windows and Linux)
* Press `Ctrl+Space` (Windows, Linux, macOS) to see a list of Markdown snippets


**Enjoy!**
