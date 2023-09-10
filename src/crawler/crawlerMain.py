#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/Crawler/main"
summary="Main code for crawling data from device"
author=Ganeshiva
created=20230820
updated=20230903
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from src.crawler.snmp import snmpWalk
from src.crawler.snmp import deviceMetric
from src.lib.yamlLib import readYamlConfig
from src.lib.printDecorator import *

import os


def readConfig(configFile="config" + os.sep + "main.yaml"):
    return readYamlConfig(configFile)


def crawlDevice(configFile):
    """
    Crawles Each Device data based on the input ConfigFile
    """
    configDirPath = os.path.dirname(configFile)
    configData = readConfig()
    deviceConfigFile = configDirPath + os.sep + configData["mainConfig"]["deviceConfig"]
    deviceConfig = readConfig(deviceConfigFile)
    devices = deviceConfig["devices"]

    for device in devices.items():
        deviceKey, deviceParameter = device[0], device[1]
        hostname, management = deviceParameter["host"], deviceParameter["management"]
        snmpConfigFile = configDirPath + os.sep + deviceParameter["config"]
        snmpConfig = readConfig(snmpConfigFile)
        ## SNMP Managed Devices
        if management == "snmp":
            printAlert("Performing SNMP walk on Host : '{}'".format(hostname))
            snmpWalkResponse = snmpWalk(hostname, snmpConfig)
            deviceMetric(snmpWalkResponse, snmpConfig["oid"])


def main():
    printBanner(codeHeader)


if __name__ == "__main__":
    main()
