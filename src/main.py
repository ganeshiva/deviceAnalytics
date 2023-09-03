#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/main"
summary="Main code for triggering the workflow"
author=Ganeshiva
created=20230820
updated=20230903
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""
import sys
import os

sys.path.append(os.getcwd())
from src.lib.printDecorator import *
from src.crawler.crawlerMain import crawlDevice

print

if __name__ == "__main__":
    argument = sys.argv
    printInfo("Input Argument(s): " + str(argument))

    if len(argument) == 2:
        # Strip \n \r Characters in the Command line
        argument = [str(i).strip("\r\n") for i in argument]
        configFile = argument[1]
        crawlDevice(configFile)
    getPrintStats()
