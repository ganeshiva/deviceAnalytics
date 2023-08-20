from pysnmp.hlapi import *
from src.lib.yamlLib import readYamlConfig
import os

def snmpConfig(configFile="config" + os.sep + "snmp.yaml"):
    return readYamlConfig(configFile)

'''
iterator = getCmd(SnmpEngine(),
          CommunityData(snmpConfig['community']),
          UdpTransportTarget((snmpConfig['host'], snmpConfig['port'])),
          ContextData(),
          ObjectType(ObjectIdentity(snmpConfig['oid'])),
          lexicographicMode=False)
'''


def perform_SNMP_Get(snmpConfig):
    for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(), 
                          CommunityData(snmpConfig['community']),
                          UdpTransportTarget((snmpConfig['host'], snmpConfig['port'])),
                          ContextData(),                                                           
                          ObjectType(ObjectIdentity(snmpConfig['oid'])),
                          lookupMib=False,
                          lexicographicMode=False):

        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break

        else:
            for varBind in varBinds:
                 print('%s = %s' % varBind)