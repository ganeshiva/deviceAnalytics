#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/src/normalizer/snmpTypeMapper"
summary="Main code for normalizer from device"
author=Ganeshiva
created=20230910
updated=20230910
cmdLine="python3 <thisScriptName> <configFile>"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from datetime import timedelta
from ipaddress import ip_address
from src.lib.printDecorator import *
import codecs


def convertType(snmpValue, snmpType):
    try:
        match snmpType:
            case "Counter32":
                """Description: Represents a non-negative integer which monotonically increases until it reaches a maximum value of 32bits-1 (4294967295 dec), when it wraps around and starts increasing again from zero."""
                return int(snmpValue)

            case "Counter64":
                """Description: The Counter64 type represents a non-negative integer which monotonically increases until it reaches a maximum value of 2^64-1 (18446744073709551615 decimal), when it wraps around and starts increasing again from zero."""
                return int(snmpValue)

            case "Gauge32":
                """Description: The Gauge32 type represents a non-negative integer, which may increase or decrease, but shall never exceed a maximum value. The maximum value can not be greater than 2^32-1 (4294967295 decimal)."""
                return int(snmpValue)

            case "Integer32":
                """Description: Signed 32bit Integer (values between -2147483648 and 2147483647)."""
                return int(snmpValue)

            case "UInteger32":
                """Description: Un signed 32bit Integer (values between 0 and 4294967295)."""
                return int(snmpValue)

            case "Integer":
                """Description: The Gauge32 type represents a non-negative integer, which may increase or decrease, but shall never exceed a maximum value. The maximum value can not be greater than 2^32-1 (4294967295 decimal)."""
                return int(snmpValue)

            case "IpAddress":
                """Description: This application-wide type represents a 32-bit internet address.  It
                is represented as an OCTET STRING of length 4, in network byte-order.

                When this ASN.1 type is encoded using the ASN.1 basic encoding rules,
                only the primitive encoding form shall be used."""
                return ip_address(snmpValue)

            case "TimeTicks":
                """Description: Represents an unsigned integer which represents the time, modulo 232 (4294967296 dec), in hundredths of a second between two epochs."""
                # printDebug(str(snmpType),str(snmpValue), timedelta(seconds=int(snmpValue)/100))
                return timedelta(seconds=int(snmpValue) / 100)

            case "OctetString":
                """Description: Arbitrary binary or textual data, typically limited to 255 characters in length."""
                return snmpValue.encode("utf-8")

            case "ObjectIdentifier":
                """Description: OID (Object Identifier) is the designation for a numeric identifier that unambiguously identifies each value in SNMP."""
                return snmpValue.encode("utf-8")

            case _:
                """Description: Default case when non of the types matches"""
                printWarning(
                    "Default handling, undefined DataType: {}, Value: {} ".format(
                        snmpType, snmpValue
                    )
                )
                return snmpValue.encode("utf-8")

    except Exception as e:
        printError(
            "Unable to Handle DataType: "
            + str(snmpType)
            + " , Value: "
            + str(snmpValue)
            + ", Exception: "
            + str(e)
        )
        return None
