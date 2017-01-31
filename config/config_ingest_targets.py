#===============================================================================
# config_ingest_targets.py for FilePusher
# 
# This validates and parses the target config file.
#
# for use with python 3.4.3
#===============================================================================
""" This module marshalls the contents of targets.yml config file into an 
object with many attributes. """
import logging
import os
import sys
import yaml
from config.log_settings import log2log

DIRECTORY = r'.\config'
CONF_FILE = 'targets.yml'
FULL_PATH = os.path.join(DIRECTORY, CONF_FILE)

class TargetsConf(object):
    
    target_list = []

    def __init__(self):
        self.target_list = []

    def config_probe(self):
        ''' Test for existence of conf file. If found, is it a file?. '''
        bReturn = False
        if not os.path.exists(FULL_PATH):
            log2log("error", DIRECTORY + "\\" + CONF_FILE + " doesn't exist.")
        elif not os.path.isfile(FULL_PATH):
            log2log("error", DIRECTORY + "\\" + CONF_FILE + " isn't a file.")
        else:
            bReturn = True
        return bReturn

    def config_ingest(self):
        ''' Read the config file, acquire info. '''
        if self.config_probe():     
            try:
                with open(FULL_PATH, 'r') as conf:
                    y = yaml.load(conf)
                    for item in y['Targets']:
                        if item['Active'] == True:
                            self.target_list.append(item)
            except OSError as ose:
                log2log("error", 'Config ingest OSError: ', str(ose))
            except:
                log2log("error", 'Config ingest Unexpected error:', sys.exc_info()[0])
        else:
            log2log("error", "There was an issue with the target config file.")
        return self.target_list

if __name__ == '__main__':
    from pprint import pprint
    MyObj = TargetsConf()
    MyObj.config_probe()
    MyObj.config_ingest()
    print('\n')
    print(vars(MyObj))
    print('\n')