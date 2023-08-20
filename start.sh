#!/usr/bin/bash

codeHeader="#################################################################
title='deviceAnalytics/start.sh'
summary='Main Execute that initates the execution'
author=Ganeshiva
created=20230820
updated=20230820
cmdLine='bash <thisScriptName>'
dependancy='python3 dependancy refer requirement.txt'
repository='https://github.com/ganeshiva/deviceAnalytics'
license='refer https://github.com/ganeshiva/deviceAnalytics/blob/main/LICENSE'
#################################################################
"

echo "${codeHeader}"

scriptCode="main.py"
configFile="config/main.yaml"

python3 ${scriptCode} ${configFile}

read -n 1 -s -r -p "Press any key to exit"
