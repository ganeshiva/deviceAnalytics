#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/src/crawler"
summary="SNMP Crawler code"
author=Ganeshiva
created=20230820
updated=20230910
cmdLine="python3 <thisScriptName> <configFile>"
dependency="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from pysnmp.hlapi import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    bulkCmd,
    nextCmd,
)

from src.normalizer.snmpTypeMapper import convertType
from src.libCommon.printDecorator import *
from datetime import datetime

import os
import sys
import time


def getOidObjectsList(snmpConfig):
    oid_Objects = [
        ObjectType(ObjectIdentity(oid)) for oid in snmpConfig["oid"]["walkOid"]
    ]
    return oid_Objects


def extractValue(varBindTable):
    """
    Extract oid, type and value from the varBindTable
    """
    oidArray = varBindTable[0][0]
    valueArray = varBindTable[0][1]
    oid = str(oidArray.prettyPrint())
    valueDict = {}

    try:
        value = valueArray.prettyPrint()
        valueType = valueArray.prettyPrintType().split(" -> ")[1]
    except Exception as e:
        printError(
            "❌ Unable to parse SNMP response: "
            + str(varBindTable)
            + ", Exception: "
            + str(e)
        )
        return None

    normalizedValue = convertType(value, valueType)
    valueDict[oid] = {"type": valueType, "value": normalizedValue}

    return valueDict


def SNMP_GetNext(hostname, snmpConfig):
    """
    Perform snmpwalk using getNext on the 'hostname' based on 'snmpConfig'
    """
    responseDict = {}

    for errorIndication, errorStatus, errorIndex, varBindTable in nextCmd(
        SnmpEngine(),
        CommunityData(snmpConfig["community"]),
        UdpTransportTarget(
            (hostname, snmpConfig["port"]),
            timeout=snmpConfig["timeout"],
            retries=snmpConfig["retries"],
        ),
        ContextData(),
        lookupMib=False,
        lexicographicMode=False,
        *getOidObjectsList(snmpConfig),
    ):
        if errorIndication:
            printError(errorIndication)
            break

        elif errorStatus:
            printError(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[int(errorIndex) - 1][0] or "?",
                ),
                file=sys.stderr,
            )
            break

        else:
            valueDict = extractValue(varBindTable)
            responseDict = responseDict | valueDict
    return responseDict


def SNMP_BulkWalk(hostname, snmpConfig):
    """
    Perform snmpwalk using getbulk on the 'hostname' based on 'snmpConfig'
    """
    responseDict = {}

    for errorIndication, errorStatus, errorIndex, varBindTable in bulkCmd(
        SnmpEngine(),
        CommunityData(snmpConfig["community"]),
        UdpTransportTarget(
            (hostname, snmpConfig["port"]),
            timeout=snmpConfig["timeout"],
            retries=snmpConfig["retries"],
        ),
        ContextData(),
        snmpConfig["nonRepeaters"],
        snmpConfig["maxRepetitions"],
        maxCalls=snmpConfig["maxCalls"],
        lookupMib=False,
        lexicographicMode=False,
        *getOidObjectsList(snmpConfig),
    ):
        if errorIndication:
            printError(errorIndication)
            break
        elif errorStatus:
            printError(
                "%s at %s"
                % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[int(errorIndex) - 1][0] or "?",
                )
            )
            break
        else:
            valueDict = extractValue(varBindTable)
            responseDict = responseDict | valueDict
    return responseDict


def snmpWalk(hostname, snmpConfig):
    """
    perform SNMP WALK based on the 'hostname' based on 'snmpConfig'
    returns result of the SNMP Walk
    """
    walkMode = snmpConfig["walkMode"]
    response = None
    startTime = time.time()
    if walkMode == "getNext":
        response = SNMP_GetNext(hostname, snmpConfig)
    elif walkMode == "bulkWalk":
        response = SNMP_BulkWalk(hostname, snmpConfig)
    endTime = time.time()
    timeElapsed = endTime - startTime
    return response, timeElapsed


def deviceSysMetric(oidDict, oidConfig):
    """
    Parse the metric response dictionary and extract metric from system level parameters
    """
    systemMetric = {}
    for metricName, oid in oidConfig["systemMetric"].items():
        systemMetric[metricName] = oidDict[oid]["value"]
    return systemMetric


def deviceSysUptime(oidDict, oidConfig):
    """
    Parse the metric response dictionary and extract Sys Uptime from parameters
    """
    return oidDict[oidConfig["sysUpTime"]]["value"]


def extractIfOidName(oidDict, interfaceNameOid):
    ifNameOidDict = {}
    interfaceNameOidPrefix = interfaceNameOid + "."
    for key, val in oidDict.items():
        if key.startswith(interfaceNameOidPrefix):
            ifNameOidDict[key.replace(interfaceNameOidPrefix, "")] = str(val["value"])
    return ifNameOidDict


def deviceInterfaceMetric(oidDict, oidConfig):
    """
    Parse the metric response dictionary and extract metrics from each interface
    """
    interfaceMetric = {}
    ifNameOid = oidConfig["interfaceName"]
    interfaceNameDict = extractIfOidName(oidDict, ifNameOid)
    for ifOid, ifName in interfaceNameDict.items():
        metricDict = {}
        for ifMetricName, ifMetricOid in oidConfig["interfaceMetric"].items():
            metricDict[ifMetricName] = oidDict[ifMetricOid + "." + ifOid]["value"]
        interfaceMetric[ifName] = metricDict

    return interfaceMetric


def deviceMetric(oidDict, oidConfig):
    """
    Parse the metric response {oidDict} dictionary and extract device metric based on oidConfig
    """
    if len(oidDict) != 0:
        deviceMetricDict = {}
        deviceMetricDict["sysMetric"] = deviceSysMetric(oidDict, oidConfig)
        deviceMetricDict["sysUpTime"] = deviceSysUptime(oidDict, oidConfig)
        deviceMetricDict["ifStats"] = deviceInterfaceMetric(oidDict, oidConfig)

        return deviceMetricDict
    else:
        return None
