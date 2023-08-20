#!/usr/bin/python3

codeHeader='''
#################################################################
title="deviceAnalytics/main"
summary="Main code for triggering the workflow"
author=Ganeshiva
created=20230820
updated=20230820
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="https://github.com/ganeshiva/deviceAnalytics"
license="refer https://github.com/ganeshiva/deviceAnalytics/blob/main/LICENSE"
#################################################################
'''

print(codeHeader)

import sys
import os
#sys.path.append("src")

print('Get current working directory : ', os.getcwd())

from src.crawler.snmp import snmpConfig
from src.crawler.snmp import perform_SNMP_Get


if __name__ == '__main__':
    argument = sys.argv
    print("Input Argument(s): " + str(argument))
        
    if len(argument) == 2 :
        # Strip \n \r Characters in the Command line
        argument = [str(i).strip("\r\n") for i in argument]
        configFile = argument[1]
        perform_SNMP_Get(snmpConfig())
        

