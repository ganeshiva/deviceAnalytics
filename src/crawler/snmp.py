#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/src/crawler"
summary="SNMP Crawler code"
author=Ganeshiva
created=20230820
updated=20230903
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
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
from src.lib.yamlLib import readYamlConfig
from src.lib.printDecorator import *

import os
import sys


def readSnmpConfig(configFile="config" + os.sep + "snmp.yaml"):
    return readYamlConfig(configFile)


def extractValue(varBindTable):
    """
    extract Value from the varBindTable
    """
    oidArray = varBindTable[0][0]
    valueArray = varBindTable[0][1]
    oid = oidArray.prettyPrint()
    valueDict = None
    try:
        value = valueArray.prettyPrint()
        valueType = valueArray.prettyPrintType().split(" -> ")[1]
    except Exception as e:
        printError("Unable to Process: " + str(varBindTable) + ", Exception: " + str(e))
        return None

    normalizedValue = normaliseValue(value, valueType)
    valueDict = {"oid": oid, "type": valueType, "value": normalizedValue}
    return valueDict


def normaliseValue(value, valueType):
    """
    format and normalise 'value' based on its 'Type'
    """
    try:
        if value == "":
            value = None
        elif valueType == "OctetString":
            value = value.encode("utf-8")
        return value
    except Exception as e:
        printError(
            "Unable to Process: "
            + str(value)
            + " , "
            + str(valueType)
            + ", Exception: "
            + str(e)
        )
        return value


def SNMP_GetNext(hostname, snmpConfig):
    """
    Perform snmpwalk using getNext on the 'hostname' based on 'snmpConfig'
    """
    resultList = []
    for errorIndication, errorStatus, errorIndex, varBindTable in nextCmd(
        SnmpEngine(),
        CommunityData(snmpConfig["community"]),
        UdpTransportTarget(
            (hostname, snmpConfig["port"]),
            timeout=snmpConfig["timeout"],
            retries=snmpConfig["retries"],
        ),
        ContextData(),
        ObjectType(ObjectIdentity(snmpConfig["oid"])),
        lookupMib=False,
        lexicographicMode=False,
    ):
        if errorIndication:
            printError(errorIndication)
            # break

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
            resultList.append(valueDict)
    return resultList


def SNMP_BulkWalk(hostname, snmpConfig):
    """
    Perform snmpwalk using getbulk on the 'hostname' based on 'snmpConfig'
    """
    resultList = []
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
        ObjectType(ObjectIdentity(snmpConfig["oid"])),
        maxCalls=snmpConfig["maxCalls"],
        lookupMib=False,
        lexicographicMode=False,
    ):
        if errorIndication:
            printError(errorIndication)
            # break
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
            resultList.append(valueDict)
    return resultList


def snmpWalk(hostname, snmpConfig):
    """
    perform SNMP WALK based on the 'hostname' based on 'snmpConfig'
    """
    snmpConfig = readSnmpConfig(snmpConfig)
    walkMode = snmpConfig["walkMode"]
    if walkMode == "getNext":
        response = SNMP_GetNext(hostname, snmpConfig)
        printInfo("getNext Responsed: {} oids".format(len(response)))
    elif walkMode == "bulkWalk":
        response = SNMP_BulkWalk(hostname, snmpConfig)
        printInfo("bulkWalk Responsed: {} oids".format(len(response)))
