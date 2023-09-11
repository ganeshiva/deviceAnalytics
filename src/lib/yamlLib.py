#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/src/lib/yamllib"
summary="Library code for yaml parsing"
author=Ganeshiva
created=20230820
updated=20230820
cmdLine="none"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

import yaml
from src.lib.printDecorator import *


def readYamlConfig(configFile):
    """
    Reading YAML file and returns as dictionary values
    """
    try:
        with open(configFile, "r", encoding="utf8") as ymlFile:
            printDebug("Reading Config File: " + str(configFile))
            ymlConfig = yaml.safe_load(ymlFile)
            return ymlConfig
    except Exception as e:
        printError(
            "Unable to Process file: " + str(configFile) + ", Exception: " + str(e)
        )
        return None
