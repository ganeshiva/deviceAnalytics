#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/store/main"
summary="Main code for storage"
author=Ganeshiva
created=20230917
updated=20230924
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from src.libCommon.yamlLib import readYamlConfig
from src.libCommon.printDecorator import *

import os
import requests
import json


def postUrlBuilder(storageConfig, deviceId):
    """
    Create URL parameters based on the configuration
    """
    url = None
    try:
        url = (
            storageConfig["postProtocol"]
            + "://"
            + storageConfig["serverHost"]
            + ":"
            + str(storageConfig["serverPort"])
            + storageConfig["prometheusUrlPath"]
            + "/"
            + storageConfig["prometheusAppName"]
            + "/instance/"
            + deviceId
        )
    except Exception as e:
        printError(
            "Unable to Process URL config "
            + str(storageConfig)
            + ", Exception: "
            + str(e)
        )
    return url


def prometheusSyntax(metricName, metricValue, labelDict=None):
    """
    Converts Metrics with labels dictionary into a Prometheus syntax
    """
    labelString = ""
    openFlowerBrace = "{"
    closeFlowerBrace = "}"
    syntaxValue = ""
    if labelDict != None:
        for label, value in labelDict.items():
            labelString += f'{label}="{value}",'
        syntaxValue = "{0}{1}{2}{3} {4}".format(
            metricName, openFlowerBrace, labelString, closeFlowerBrace, metricValue
        )
    else:
        syntaxValue = "{0} {1}".format(metricName, metricValue)
    return syntaxValue


def genSysUptimeMetric(sysUpTime):
    """
    Generate System Uptim Metric in Prometheus syntax
    """
    metricName = "sysUpTime"
    return prometheusSyntax(metricName, sysUpTime)


def genSysMetric(sysDict):
    """
    Generate System Metric in Prometheus syntax
    """
    metricName = "sys"
    metricValue = 1
    labelDict = {}
    for labelName, labelValue in sysDict.items():
        labelDict[labelName] = labelValue
    return prometheusSyntax(metricName, metricValue, labelDict)


def genInterfaceMetric(interfaceDict):
    """
    Generate Interface Metrics in Prometheus syntax
    """
    prometheusPayload = ""
    try:
        for interfaceName, interfaceMetric in interfaceDict.items():
            labelDict = {"ifName": interfaceName}
            for metricName, metricValue in interfaceMetric.items():
                prometheusPayload += (
                    prometheusSyntax(metricName, metricValue, labelDict) + "\n"
                )
    except Exception as e:
        printError(
            "Unable to Process : " + str(interfaceDict) + ", Exception: " + str(e)
        )
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    return prometheusPayload


def httpPostToStorage(deviceId, url, payload):
    """
    Utility on perform REST call to store metric payload
    """
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    try:
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code == 200:
            printSuccess(
                "✅ "
                + deviceId
                + ": Pushed to Store , Payload Length: "
                + str(len(payload))
            )
        else:
            printFailure("❌ Response Code: " + str(r.status_code))
            printError("Error Response: " + str(r.json()))
    except Exception as e:
        printFailure(
            "❌ Unable to Post device : "
            + str(deviceId)
            + " data to storage, Exception: "
            + str(e)
        )


def postSysData(timestamp, deviceId, dataDict, storageConfig):
    """
    Post the System metric data to store via REST call
    """
    url = postUrlBuilder(storageConfig, deviceId)

    if url != None:
        try:
            payload = genSysMetric(dataDict) + " " + str(timestamp)
            httpPostToStorage(deviceId, url, payload)
        except Exception as e:
            printError(
                "Unable to Process for Storage : "
                + str(storageConfig)
                + ", Exception: "
                + str(e)
            )
    else:
        printFailure("❌ Invalid URL input!")


def postData(timestamp, deviceId, dataDict, storageConfig):
    """
    Post the metric data to store via REST call
    """
    url = postUrlBuilder(storageConfig, deviceId)

    if url != None:
        try:
            sysUpTimeMetric = genSysUptimeMetric(dataDict["sysUpTime"])
            interfaceMetric = genInterfaceMetric(dataDict["ifStats"])
            payload = (
                sysUpTimeMetric
                + "\n"
                + interfaceMetric.strip("\n")
                + " "
                + str(timestamp)
            )
            httpPostToStorage(deviceId, url, payload)
        except Exception as e:
            printError(
                "Unable to Process for Storage : "
                + str(storageConfig)
                + ", Exception: "
                + str(e)
            )
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    else:
        printFailure("❌ Invalid URL input!")


def main():
    printBanner(codeHeader)


if __name__ == "__main__":
    main()
