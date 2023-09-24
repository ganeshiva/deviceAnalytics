import datetime
import logging
import logging.handlers
import os
import inspect
import sys

enableLog = True

logFolder = "logs"
logFilePrefix = os.path.basename(os.path.realpath(sys.argv[0]))  # main fileName
logFileExtension = ".log"
fileTimestampFormat = "_%Y_%_b_%d_%H_%M_%S"
loggerMessageFormat = '%(asctime)s:%(name)s:%(levelname)s:[%(filename)s:%(lineno)s-%(funcName)s()]: "%(message)s"'
loggerDateFormat = "%Y-%b-%d/%H:%M:%S/%z"

if enableLog == True:
    try:
        currentTimestamp = datetime.datetime.now().strftime(fileTimestampFormat)
        curpath = os.path.abspath(os.curdir)
        if os.path.isdir(logFolder) == False:
            os.mkdir(logFolder)
        logFileName = os.path.abspath(
            os.path.join(
                curpath, logFolder, logFilePrefix + currentTimestamp + logFileExtension
            )
        )
        logging.basicConfig(
            handlers=[
                logging.handlers.RotatingFileHandler(
                    logFileName, maxBytes=1000000, backupCount=10
                )
            ],
            format=loggerMessageFormat,
            level=logging.INFO,
            datefmt=loggerDateFormat,
        )
        logging.info("Logging Initiated Successfully: " + str(logFileName))
        print("Logging Initiated Successfully: " + str(logFileName))
    except Exception as e:
        print(inspect.stack()[0][3] + " Exception: " + str(e))
        print("Abnormal Exit!!")
        exit(1)
else:

    class dummyLogger:
        def debug(message, *xArg):
            None
            # Do Nothing

        def error(message):
            None
            # Do Nothing

        def warning(message):
            None
            # Do Nothing

        def critical(message):
            None
            # Do Nothing

        def info(message, *xArg):
            None
            # Do Nothing

    logging = dummyLogger()
