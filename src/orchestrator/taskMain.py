#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/orchestrator/main"
summary="Main code for orchestrating the process"
author=Ganeshiva
created=20230917
updated=20230924
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from src.crawler.crawlerMain import crawlDevice
from src.store.storage import postData
from src.store.storage import postSysData
from src.libCommon.yamlLib import readYamlConfig
from src.libCommon.printDecorator import *
from datetime import datetime

import concurrent.futures
import time
import os


def readDeviceConfig(configFile):
    """
    Read YAML config file
    """
    devicesDict = None
    configDirPath = os.path.dirname(configFile)
    configData = readYamlConfig(configFile)
    deviceConfigFile = configDirPath + os.sep + configData["mainConfig"]["deviceConfig"]
    deviceConfig = readYamlConfig(deviceConfigFile)
    devicesDict = deviceConfig["devices"]
    return devicesDict


def readParralismConfig(configFile):
    """
    Read Parallel config file
    """
    parallelTask, parallelTaskTimeout = None, None
    configData = readYamlConfig(configFile)
    parallelTask = configData["mainConfig"]["parallelTask"]
    parallelTaskTimeout = configData["mainConfig"]["parallelTaskTimeout"]
    return (parallelTask, parallelTaskTimeout)


def collectAndStoreDeviceSysParam(deviceConfig):
    """
    Collect System Metrics and Store
    """
    deviceId = deviceConfig[0]
    printInfo(
        "ℹ️ "
        + str(deviceId)
        + ": Collecting Device System Parameters : CurrentTime: "
        + str(datetime.now())
    )
    timestamp = datetime.now().timestamp() * 1000
    response = crawlDevice(deviceConfig)
    sysResponse = response["sysMetric"]

    if response != None:
        storageConfig = readYamlConfig(deviceConfig[1]["storage"])
        postSysData(timestamp, deviceId, sysResponse, storageConfig)


def collectAndStoreTask(deviceConfig):
    """
    Collect Metrics and Store
    """
    deviceId = deviceConfig[0]
    printInfo(
        "🏹 " + str(deviceId) + ": Initiating Crawling Task : " + str(datetime.now())
    )
    timestamp = datetime.now().timestamp() * 1000
    response = crawlDevice(deviceConfig)
    monitoringInterval = deviceConfig[1]["monitoringInterval"]

    if response != None:
        storageConfig = readYamlConfig(deviceConfig[1]["storage"])
        postData(timestamp, deviceId, response, storageConfig)

    printAlert(
        "😴 "
        + str(deviceId)
        + ": Crawler Sleeping : "
        + str(monitoringInterval)
        + "(s) 💤"
    )
    time.sleep(monitoringInterval)


def initDataCollection(configFile):
    """
    Crawles Each Device data based on the input ConfigFile
    """
    devicesConfig = readDeviceConfig(configFile)
    parallelTask, parallelTaskTimeout = readParralismConfig(configFile)
    for devConfig in devicesConfig.items():
        collectAndStoreDeviceSysParam(devConfig)
    while True:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=parallelTask
        ) as executor:
            executor.map(
                collectAndStoreTask, devicesConfig.items(), timeout=parallelTaskTimeout
            )


def main():
    printBanner(codeHeader)


if __name__ == "__main__":
    main()
