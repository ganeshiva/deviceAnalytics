import yaml
from src.libCommon.printDecorator import *


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
