#===============================================================================
# pre_copy_thread.py for FilePusher
# 
# This holds the queue and the process that operate on the files aquired by the
# watch folder.  This file handles the processes before the copy.
#
# for use with python 3.5
#===============================================================================
import time
import re
import os
import copy_thread
import shutil as su
import file_and_folder
import traceback
import datetime
from multiprocessing import Queue
from threading import Thread
from xml_parse.smil_file_parser import SmilParse
from config.config_ingest_service import ServiceConf
from config.log_settings import log2log
from file_and_folder import FolderObject

import_queue = Queue(200)


class ImportValidationThread(Thread):
    ''' This class ingests the items from the import queue. '''
    def __init__(self, group = None, target = None, name = None, args = (), 
                 kwargs = None, daemon = None):
        super(ImportValidationThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            try:
                conf_service = ServiceConf()
                for product in conf_service.product_list:
                    #print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + 
                    #     " Searching " + str(product['WatchPath']))
                    
                    for file in os.scandir(str(product['WatchPath'])):
                        if file.is_file():
                            if (str(r"*" + os.path.splitext(file.name)[1]) == str(product['WatchPattern'])):
                                log2log('debug', "made inside pattern test.")
                                file_stub = str(file.name).split('-')[0]
                                file_path = os.path.dirname(file.path)
                                temp_file_dest = conf_service.temp_move_path + file_stub
                                
                                log2log('debug', "File stub: " + file_stub)
                                log2log('debug', "File path: " + file_path)
                                log2log('debug', "temp file dest: "+ temp_file_dest)
                                
                                if not bool(product['SingleFiles']) and bool(product['ValidateViaSmil']):
                                    log2log('debug', "made it to smil check.")
                                    temp_check = FolderObject(file.name, file.path)
                                    smil_check = SmilParse(temp_check)
                                    if smil_check.smil_probe():
                                        log2log('debug', "Smil check passed.")
                                        
                                        # move the files to the temp folder                                                                       
                                        if os.path.exists(temp_file_dest):
                                            su.rmtree(temp_file_dest, ignore_errors=True)
                                        os.mkdir(temp_file_dest)                                                                
                                        for streamfile in smil_check.smil_dereference():
                                            filename = os.path.basename(streamfile)
                                            log2log('debug', "Move check: " + file_path + "\\" + filename)
                                            su.move(file_path + "\\" + filename,
                                                    temp_file_dest + "\\" + filename)                               
                                        su.move(file_path + "/" + file.name, temp_file_dest + "/" + file.name)
                                        
                                        log2log("info","Adding " + file.name + " to the work queue.")
                                        print("Adding " + file.name + " to the work queue.")
                                        temp_entry = FolderObject(file.name, temp_file_dest + "/" + file.name)   
                                        copy_thread.work_queue.put(temp_entry)                             
                                        
                                elif bool(product['SingleFiles']):
                                    regex = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]+-[0-9]{3,4}_[0-9]{3,4}x[0-9]{3,4}.mp4$'
                                    if re.search(regex, file.name):
                                        su.move(file_path + "/" + file.name, temp_file_dest)
                                        log2log("debug","Adding " + file.name + " to the copy queue.")
                                        print("Adding " + file.name + " to the copy queue.")
                                        copy_thread.work_queue.put(FileObject(file.name, file.path))
                                    else:
                                        log2log("error", item.name + " has an invalid filename.")
                    log2log('debug', "Time to sleep.")
                    time.sleep(15)
            except Exception as ex:
                log2log('error', "Queue creator exception: " + str(ex))
                log2log('error', traceback.format_exc())