#!/usr/bin/python3

codeHeader = """
#################################################################
title="deviceAnalytics/src/lib/printDecorator"
summary="Libaray code to prints with ANSI color and also send the message to logger for file logging"
author=Ganeshiva
created=20230910
updated=20230910
cmdLine="none"
dependancy="refer requirements.txt"
repository="refer repository.txt"
license="refer LICENSE"
#################################################################
"""

from src.lib.logManager import *

global printStats


def initPrintStats():
    global printStats
    # Initializing Print Statistics
    printStats = {
        "banner": 0,
        "error": 0,
        "success": 0,
        "failure": 0,
        "info": 0,
        "debug": 0,
        "alert": 0,
        "warning": 0,
    }


initPrintStats()


def getPrintStats():
    global printStats
    statsString = ""
    for key, value in printStats.items():
        statsString += str(key) + ":" + str(value) + ", "
    print("Logging Statistics: " + statsString)


# Print Color Constants

ENDC = "\033[m"  # reset to the defaults
TWHITE = "\033[37m"

COLOR_BRIGHT_GREEN = "\033[1;32;40m"  # Green Text
COLOR_BRIGHT_RED = "\033[1;31;40m"  # Bright RED Text
COLOR_YELLOW_BG = "\033[33;5;7m"  #
COLOR_BRIGHT_CYAN = "\033[1;36;40m"  # Bright Cyan
COLOR_BRIGHT_MAGENTA = "\033[1;35;40m"  # Bright Magenta
COLOR_DARK_GREY = "\033[1;30;40m"  # Bright Magenta

Bold = "\x1b[1m"
Dim = "\x1b[2m"
Italic = "\x1b[3m"
Underlined = "\x1b[4m"
Blink = "\x1b[5m"
Reverse = "\x1b[7m"
Hidden = "\x1b[8m"
# Reset part
Reset = "\x1b[0m"
Reset_Bold = "\x1b[21m"
Reset_Dim = "\x1b[22m"
Reset_Italic = "\x1b[23m"
Reset_Underlined = "\x1b[24"
Reset_Blink = "\x1b[25m"
Reset_Reverse = "\x1b[27m"
Reset_Hidden = "\x1b[28m"

# Foreground
F_Default = "\x1b[39m"
F_Black = "\x1b[30m"
F_Red = "\x1b[31m"
F_Green = "\x1b[32m"
F_Yellow = "\x1b[33m"
F_Blue = "\x1b[34m"
F_Magenta = "\x1b[35m"
F_Cyan = "\x1b[36m"
F_LightGray = "\x1b[37m"
F_DarkGray = "\x1b[90m"
F_LightRed = "\x1b[91m"
F_LightGreen = "\x1b[92m"
F_LightYellow = "\x1b[93m"
F_LightBlue = "\x1b[94m"
F_LightMagenta = "\x1b[95m"
F_LightCyan = "\x1b[96m"
F_White = "\x1b[97m"
# Background
B_Default = "\x1b[49m"
B_Black = "\x1b[40m"
B_Red = "\x1b[41m"
B_Green = "\x1b[42m"
B_Yellow = "\x1b[43m"
B_Blue = "\x1b[44m"
B_Magenta = "\x1b[45m"
B_Cyan = "\x1b[46m"
B_LightGray = "\x1b[47m"
B_DarkGray = "\x1b[100m"
B_LightRed = "\x1b[101m"
B_LightGreen = "\x1b[102m"
B_LightYellow = "\x1b[103m"
B_LightBlue = "\x1b[104m"
B_LightMagenta = "\x1b[105m"
B_LightCyan = "\x1b[106m"
B_White = "\x1b[107m"


def printBanner(message):
    global printStats
    print(
        COLOR_BRIGHT_GREEN
        + "/*****************************************************************/"
        + ENDC
    )
    print(B_Black + Bold + Italic + F_Green + Blink + str(message) + ENDC)
    print(
        COLOR_BRIGHT_GREEN
        + "/*****************************************************************/"
        + ENDC
    )
    printStats["banner"] += 1
    logging.info("/*****************************************************************/")
    logging.info(message)
    logging.info("/*****************************************************************/")


def printError(message):
    global printStats
    print(COLOR_BRIGHT_MAGENTA + str(message) + Reset)
    logging.error(message)
    printStats["error"] += 1


def printSuccess(message):
    global printStats
    print(COLOR_BRIGHT_GREEN + str(message) + Reset)
    logging.info(message)
    printStats["success"] += 1


def printFailure(message):
    global printStats
    print(COLOR_BRIGHT_RED + str(message) + Reset)
    logging.critical(message)
    printStats["failure"] += 1


def printInfo(message):
    global printStats
    print(B_Black + F_White + str(message) + Reset)
    logging.info(message)
    printStats["info"] += 1


def printDebug(message):
    global printStats
    # print( COLOR_DARK_GREY + str(message) + ENDC)
    logging.debug(message)
    printStats["debug"] += 1


def printAlert(message):
    global printStats
    print(COLOR_BRIGHT_GREEN + Blink + str(message) + Reset)
    logging.info("Alert: " + message)
    printStats["alert"] += 1


def printWarning(message):
    global printStats
    print(COLOR_BRIGHT_MAGENTA + Blink + str(message) + Reset)
    logging.warning(message)
    printStats["warning"] += 1
