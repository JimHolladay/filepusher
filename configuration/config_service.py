# ==============================================================================
# config_service.py
#
# This module marshals the contents of service.yml configuration file into an object
# with many attributes.
#
# Written with/for Python 3.4.3.
# ==============================================================================
""" This module will marshal the contents of the service configuration file (service.yml)."""
import os
import sys
from pprint import pprint

import yaml

from .log_settings import log2log

DIRECTORY = r'.\config'
CONF_FILE = 'service.yml'
FULL_PATH = os.path.join(DIRECTORY, CONF_FILE)


class ServiceConf(object):
    """ This class ingests the service."""
    def __init__(self):
        self.db_user = ''
        self.db_name = ''
        self.db_address = ''
        self.machine_free_space_min = 0
        self.concurrent_copies = 0
        self.product_list = []
        self.error_email_list = []
        self.error_slack_list = []
        self.error_sms_list = []
        self.admin_email_list = []
        self.admin_slack_list = []
        self.admin_sms_list = []
        self.temp_move_path = ''
        self.config_ingest()

    def config_ingest(self):
        """ Read the configuration file, acquire info. """
        try:
            with open(FULL_PATH, 'r') as conf:
                yaml_file = yaml.load(conf)
                self.db_user = yaml_file['Database']['DBUser']
                self.db_name = yaml_file['Database']['DBName']
                self.db_address = yaml_file['Database']['DBAddr']
                self.temp_move_path = yaml_file['Folders']['TempMoveFolder']
                self.machine_free_space_min = yaml_file['Machine']['FreeSpace']
                self.concurrent_copies = yaml_file['Threads']['ConcurrentCopies']
                for item in yaml_file['Products']:
                    self.product_list.append(item)

                for item in yaml_file['Notify']:
                    if item['Errors'][0]['Email'] is True:
                        self.error_email_list.append(item['Email'])
                    if item['Errors'][0]['Slack'] is True:
                        self.error_slack_list.append(item['Slack'])
                    if item['Errors'][0]['SMS'] is True:
                        self.error_sms_list.append(item['SMS'])
                    if item['Admin'][0]['Email'] is True:
                        self.admin_email_list.append(item['Email'])
                    if item['Admin'][0]['Slack'] is True:
                        self.admin_slack_list.append(item['Slack'])
                    if item['Admin'][0]['SMS'] is True:
                        self.admin_sms_list.append(item['SMS'])
        except OSError as ose:
            log2log("error", 'OSError: ' + str(ose))
        except Exception:
            log2log("error", 'Unexpected exception:' + sys.exc_info()[0])


def config_probe():
    """ Test for existence of conf file. If found, is it a file?. """
    try:
        os.path.exists(FULL_PATH)
        try:
            os.path.isfile(FULL_PATH)
        except OSError as ose:
            log2log("error", 'OSError: ' + str(ose))
    except OSError as ose:
        log2log("error", 'OSError: ' + str(ose))

if __name__ == '__main__':
    TEST_OBJ = ServiceConf()
    config_probe()
    TEST_OBJ.config_ingest()
    print('\n')
    pprint(vars(TEST_OBJ))
    print('\n')
