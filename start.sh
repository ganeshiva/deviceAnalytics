#!/usr/bin/bash

codeHeader="#################################################################
title='deviceAnalytics/start.sh'
summary='Main Execute that initates the execution'
author=Ganeshiva
created=20230820
updated=20230903
cmdLine='bash <thisScriptName>'
dependancy='python3 dependancy refer requirement.txt'
repository='refer repository.txt'
license='refer LICENSE'
#################################################################
"

echo "${codeHeader}"

scriptCode="src/main.py"
configFile="config/main.yaml"

python3 ${scriptCode} ${configFile}
echo -e "Program ended!!"
