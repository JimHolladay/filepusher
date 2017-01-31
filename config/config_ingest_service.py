#==============================================================================
# config_ingest_service.py
#
# This module marshalls the contents of service.yml config file into an object
# with many attributes.
#
# Written with/for Python 3.4.3.
#==============================================================================
import os
import sys
import yaml
from config.log_settings import log2log

DIRECTORY = r'.\config'
CONF_FILE = 'service.yml'
FULL_PATH = os.path.join(DIRECTORY, CONF_FILE)

class ServiceConf(object):

    def __init__(self):
        self.db_user = ''
        self.db_name = ''
        self.db_addr = ''
        self.machine_freespace_min = 0
        self.concurrent_copies = 0
        self.product_list = []
        self.error_email_list = []
        self.error_slack_list = []
        self.error_sms_list = []
        self.admin_email_list = []
        self.admin_slack_list = []
        self.admin_sms_list = []        
        self.temp_move_path = ''        
        self._config_probe()
        self._config_ingest()

    def _config_probe(self):
        ''' Test for existence of conf file. If found, is it a file?. '''
        try:
            os.path.exists(FULL_PATH)
            try:
                os.path.isfile(FULL_PATH)
            except OSError as ose:
                log2log("error", 'OSError: ', str(ose))
        except OSError as ose:
            log2log("error", 'OSError: ', str(ose))

    def _config_ingest(self):
        ''' Read the config file, acquire info. '''
        try:
            with open(FULL_PATH, 'r') as conf:
                y = yaml.load(conf)
        except OSError as ose:
            log2log("error", 'OSError: ', str(ose))
        except:
            log2log("error", 'Unexpected error:', sys.exc_info()[0])

        self.db_user = y['Database']['DBUser']
        self.db_name = y['Database']['DBName']
        self.db_addr = y['Database']['DBAddr']
        self.temp_move_path = y['Folders']['TempMoveFolder']
        self.machine_freespace_min = y['Machine']['FreeSpace']
        self.concurrent_copies = y['Threads']['ConcurrentCopies']
        for item in y['Products']:
            self.product_list.append(item)

        for item in y['Notify']:
            if item['Errors'][0]['Email'] == True:
                self.error_email_list.append(item['Email'])
            if item['Errors'][0]['Slack'] == True:
                self.error_slack_list.append(item['Slack'])
            if item['Errors'][0]['SMS'] == True:
                self.error_sms_list.append(item['SMS'])
            if item['Admin'][0]['Email'] == True:
                self.admin_email_list.append(item['Email'])
            if item['Admin'][0]['Slack'] == True:
                self.admin_slack_list.append(item['Slack'])
            if item['Admin'][0]['SMS'] == True:
                self.admin_sms_list.append(item['SMS'])

if __name__ == '__main__':
    from pprint import pprint
    MyObj = ServiceConf()
    MyObj.config_probe()
    MyObj.config_ingest()
    print('\n')
    pprint(vars(MyObj))
    print('\n')    