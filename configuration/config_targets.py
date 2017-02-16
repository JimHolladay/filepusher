# ===============================================================================
# config_targets.py for FilePusher
#
# This validates and parses the target configuration file.
#
# for use with python 3.4.3
# ===============================================================================
""" This module marshalls the contents of targets.yml configuration file into an
object with many attributes. """
import os
import sys
import yaml

from .log_settings import log2log

DIRECTORY = r'.\config'
CONF_FILE = 'targets.yml'
FULL_PATH = os.path.join(DIRECTORY, CONF_FILE)


class TargetsConf(object):
    """ Class that reads in the target configuration file. """
    target_list = []

    def __init__(self):
        self.target_list = []

    def config_ingest(self):
        """ Read the configuration file, acquire info. """
        if config_probe():
            try:
                with open(FULL_PATH, 'r') as conf:
                    target_config = yaml.load(conf)
                    for item in target_config['Targets']:
                        if item['Active'] is True:
                            self.target_list.append(item)
            except OSError as ose:
                log2log("error", 'Config ingest OSError: ' + str(ose))
            except Exception:
                log2log("error", 'Config ingest Unexpected error:' + sys.exc_info()[0])
        else:
            log2log("error", "There was an issue with the target configuration file.")
        return self.target_list


def config_probe():
    """ Test for existence of conf file. If found, is it a file?. """
    b_return = False
    if not os.path.exists(FULL_PATH):
        log2log("error", DIRECTORY + "\\" + CONF_FILE + " doesn't exist.")
    elif not os.path.isfile(FULL_PATH):
        log2log("error", DIRECTORY + "\\" + CONF_FILE + " isn't a file.")
    else:
        b_return = True
    return b_return

if __name__ == '__main__':
    TEST_OBJ = TargetsConf()
    config_probe()
    TEST_OBJ.config_ingest()
    print('\n')
    print(vars(TEST_OBJ))
    print('\n')
