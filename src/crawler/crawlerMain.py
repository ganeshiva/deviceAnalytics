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
from src.libCommon.yamlLib import readYamlConfig
from src.libCommon.printDecorator import *

import os


def crawlDevice(deviceConfig):
    """
    Crawles Device data based on the input deviceParameter
    """
    try:
        deviceKey, deviceParameter = deviceConfig[0], deviceConfig[1]
        hostname, management = deviceParameter["host"], deviceParameter["management"]
        snmpConfigFile = deviceParameter["config"]
        snmpConfig = readYamlConfig(snmpConfigFile)
        ## SNMP Managed Devices
        if management == "snmp":
            printInfo("🚶 {}: Performing SNMP Walk".format(deviceKey))
            snmpWalkResponse, timeElapsed = snmpWalk(hostname, snmpConfig)
            printInfo(
                "✅ {}: SNMP Walk responded: {} oids, took {} (s)".format(
                    deviceKey, len(snmpWalkResponse), timeElapsed
                )
            )
            return deviceMetric(snmpWalkResponse, snmpConfig["oid"])

    except Exception as e:
        printFailure(
            "Unable to Crawl Device: " + str(deviceKey) + ", Exception: " + str(e)
        )
        return None


def main():
    printBanner(codeHeader)


if __name__ == "__main__":
    main()
