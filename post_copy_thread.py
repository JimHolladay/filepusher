#===============================================================================
# post_copy_thread.py for FilePusher
# 
# This holds the queue and the process that happens after the copy process.
#
# for use with python 3.5
#===============================================================================
import time
import shutil as su
import copy_thread
import datetime
import os
import socket
from multiprocessing import Queue
from threading import Thread
from xml_parse.smil_file_parser import SmilParse
from config.log_settings import log2log
from file_and_folder import FolderObject
from csvlogger import csv_log_queue

post_work_queue = Queue(100)

class PostProducerThread(Thread):
    ''' This class does the post copy work on the post_work_queue. '''
    def __init__(self, group = None, target = None, name = None, args = (), 
                 kwargs = None, daemon = None):
        super(PostProducerThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not post_work_queue.empty():
                item = post_work_queue.get()              
                log2log("debug", 'Post Producer Popped ' + item.name)
                source_folder = os.path.dirname(item.full_path)
                file_stub = item.name.split('-')[0]
                
                log2log('debug', "Testing post item: " + str(item.target))    
                
                if type(item) is FolderObject:
                    smil_check = SmilParse(item)
                    print("Validating " + item.name + "...")
                    if smil_check.smil_probe():
                        log2log("debug", "Smil check passed. Deleting temp folder: " + 
                                os.path.dirname(item.full_path))
                        su.rmtree(os.path.dirname(item.full_path))
                        
                        # Write entries to the csv log
                        file_list = smil_check.smil_dereference()                        
                        statinfo = os.stat(item.destination + item.name)
                        csv_string = ("Finished, " + item.finish_time.strftime("%Y-%m-%d") + "," +
                            item.finish_time.strftime("%H:%M:%S") + "," +
                            socket.gethostname() + "," + file_stub + "," + 
                            item.name + "," + str(statinfo.st_size) + "," + 
                            item.target['Name'] + "\n")
                                                 
                        for file in file_list:
                            statinfo = os.stat(file)
                            filename = os.path.basename(file)                                
                            csv_string += ("Finished, " + item.finish_time.strftime("%Y-%m-%d") + "," +
                                item.finish_time.strftime("%H:%M:%S") + "," +
                                socket.gethostname() + "," + file_stub + "," + 
                                filename + "," + str(statinfo.st_size) + "," + 
                                item.target['Name'] + "\n")
                        csv_log_queue.put(csv_string)
                        
                        print(item.name + " is finished moving.")                                                
                    else:
                        # Copy Validation failed.
                        log2log("debug", "Smil check failed. Sending back to the copy queue.")
                        copy_thread.work_queue.put(item)
                else: 
                    # Single file copy cleanup
                    if os.path.isfile(item.destination + item.name):
                        statinfo = os.stat(item.destination + item.name)
                        os.remove(source_folder+ "\\" + item.name)
                        print(item.name + " is finished.")
                        log2csv("Finished", source_folder, item.name, 
                                    statinfo.st_size, item.target['Name'],
                                    item.finish_time)
                    else: # file copy failed
                        log2log("debug", "File copy failed. Sending back to the copy queue.")
                        copy_thread.work_queue.put(item)
            else:
                time.sleep(1)