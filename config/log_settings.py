#===============================================================================
# log_settings.py for FilePusher
#
# This is the class that controls the log config settings and ingest..
#
# for use with python 3.5
#===============================================================================
import yaml
import logging
import os
import socket
import datetime
import time
from pip._vendor.cachecontrol._cmd import setup_logging

def log2log(logtype, msg):
    try:
        debuglog = logging.getLogger('full-log')
        logfilename = 'Z:/Logs/filepusher/log-' + datetime.date.today().strftime('%Y-%m-%d') + ".txt"
        debugloghandler = logging.handlers.RotatingFileHandler(filename=logfilename,
                                                               maxBytes=500000,
                                                               backupCount=365,
                                                               encoding='utf8')
        debugloghandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        if not debuglog.hasHandlers():
            debuglog.addHandler(debugloghandler)
        debuglog.setLevel(logging.DEBUG)
        if logtype == 'debug':
            debuglog.debug(msg)
        elif logtype == 'info':
            debuglog.info(msg)
        elif logtype == 'warning':
            debuglog.warning(msg)
        elif logtype == 'error':
            debuglog.error(msg)
        else:
            print("Error in log generation.")
        debugloghandler.close()
        debuglog.removeHandler(debugloghandler)
    except Exception as ex:
        print("Log2Log Exception happened: " + str(ex))
        
if __name__ == '__main__':
    log2csv("Started", "Movies", "this_is_a_file.txt", 987654321, "Vidstorage", 
            datetime.datetime.now())
    log2log('debug', "This is just a test.")