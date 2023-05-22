import os
import re
import pdb
import datetime


def close_file(self, instruction, markdown):
    markdown = Writer._cleanup_hyphens(markdown)
    filename = (('./output/' + str(instruction).replace('/', '_').replace(' ', '_')) + '.md')
    print(('writing ' + filename))
    fwrite = open(filename, 'w')
    now = datetime.datetime.now()
    generatedTime = ((((str(now.day) + '-') + str(now.month)) + '-') + str(now.year))
    markdown += (((('\n --- \n<p align="right"><i>Source: ' + self.source) + '<br>Generated: ') + generatedTime) + '</i></p>\n')
    fwrite.write(markdown)
    fwrite.close()
