#!/bin/bash
cd ..
mvn clean package
time mvn exec:java -Dexec.mainClass=ConvertJava -Dexec.args="root plt.plot/snippets.json plt.plot"
time mvn exec:java -Dexec.mainClass=ConvertJava -Dexec.args="root plt.plot/test.json plt.plot/test.py"
time python3 src/main/python/similar.py -c plt.plot/snippets.json -d plt.plot/tmpout
time python3 src/main/python/similar.py -d plt.plot/tmpout -f plt.plot/test.json -o plt.plot/output.txt
