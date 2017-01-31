#===============================================================================
# copy_thread.py for FilePusher/cs2v
# 
# This holds the queue and the process for the copying of files.
#
# for use with python 3.5
#===============================================================================
import os
import shutil as su
import post_copy_thread
import datetime
import traceback
import socket
from subprocess import call
from time import sleep, mktime
from multiprocessing import Process, Queue, freeze_support, active_children
from xml_parse.smil_file_parser import SmilParse
from threading import Thread
from config.config_ingest_targets import TargetsConf
from config.config_ingest_service import ServiceConf
from config.log_settings import log2log
from file_and_folder import FolderObject
from csvlogger import csv_log_queue

work_queue = Queue(100)
_task_queue = Queue(50)
_done_queue = Queue(50)

def _worker(input, output):
    item = input.get()    
    if type(item) is FolderObject:
        source_folder = os.path.dirname(item.full_path)
        lastfolder = os.path.basename(os.path.dirname(item.full_path))
        print("Copying... " + lastfolder + " to " + item.destination)
        if os.path.exists(item.destination):
            log2log('debug', 'Trying to delete target folder: ' + item.destination)
            su.rmtree(item.destination)
        _copyafolder(source_folder, item.destination)
    else:
        print("Copying... " + os.path.basename(item.full_path) + " to " + 
              item.destination)
        _copyafile(item.full_path, item.destination)        
    output.put(item)

def _copyafile(source, destination):
    ''' This function will copy a single file from source to destination.'''
    # For use with legacy vidstager script
    call(["robocopy", os.path.dirname(source), destination, os.path.basename(source), 
          "/S", "/NJH", "/NP", "/NJS", "/NFL", "/NC", "/NDL", "/IS", "/XJ"])
    
    # For future Use when vidstagers are moved to python
    #su.copy2(source, destination)

def _copyafolder(source, destination):
    ''' This function will copy a folder from source to destination.'''
    # this is to be removed when the vidstager script is moved to python
    call(["robocopy", source, destination,  
      "/S", "/NJH", "/NP", "/NJS", "/NFL", "/NC", "/NDL", "/IS", "/XJ"])
    
    # This is for when the vidstage script is moved to python
    #su.copytree(source, destination)

class ProducerThread(Thread):
    ''' This class does the work of copying files. '''

    def __init__(self, group = None, target = None, name = None, args = (), 
                 kwargs = None, daemon = None):
        super(ProducerThread, self).__init__()
        self.name = name
        self.target_count = dict()
        self._zero_target_dict()
        self._target_hold = None

    def _get_target(self):
        ''' This method will choose the target for the copy item. '''
        count = 100
        return_target = None
        try:
            # Try not to use the same target as last time (target_hold)
            for x in range(1,2):
                targets = TargetsConf().config_ingest()
                log2log("debug", "Get Target Counts: " + str(self.target_count))
                if len(targets) > 0:
                    for target in targets:
                        log2log('debug', "target_hold = " + str(self._target_hold))
                        if (self.target_count[target['Name']] < count and
                            self.target_count[target['Name']] < target['CopyCount'] and
                            target['Name'] != self._target_hold):
                            count = self.target_count[target['Name']]
                            return_target = dict()
                            return_target = target
    
                    if return_target == None:
                        self._target_hold = None
                    else:
                        break
                else:
                    log2log('error', "No targets found.")
        except Exception as ex: 
            print("Get target Exception: " + str(ex))
        self._target_hold = return_target
        return return_target
    
    def _zero_target_dict(self):
        ''' This method clears the target counts to what is currently active. '''
        try: 
            for target in TargetsConf().config_ingest():
                if target['Active']:
                    self.target_count.update({target["Name"]: 0})
            print("Target Dictionary: " + str(self.target_count))
        except Exception as ex:
            print("Clear count Exception: " + str(ex))
     
    def run(self):
        freeze_support()
        process_list = ['fakevalue']        
        
        while True:
            
            if not work_queue.empty():
                service_conf = ServiceConf()
                num_of_processes = ServiceConf().concurrent_copies
                
                # Load the copy task queue
                try:
                    item = work_queue.get()
                    log2log('debug', 'Producer Popped ' + item.name)                 
                    
                    file_path = os.path.dirname(item.full_path)
                    file_stub = item.name.split('-')[0]
                    
                    # Get the target path
                    target = self._get_target()
                    if not target == None:
                        
                        log2log("debug", "Sending to target: " + str(target))
                        item.target = target
                        self.target_count[target['Name']] += 1                   
                        item.start_time = datetime.datetime.now()
                        source_folder = os.path.dirname(item.full_path)
                    
                        # Create string for the CSV log file
                        statinfo = os.stat(item.full_path)
                        csv_string = ("Started, " + item.start_time.strftime("%Y-%m-%d") + "," +
                            item.start_time.strftime("%H:%M:%S") + "," +
                            socket.gethostname() + "," + file_stub + "," + 
                            item.name + "," + str(statinfo.st_size) + "," + 
                            target['Name'] + "\n")
                        if type(item) is FolderObject:                             
                            log2log("debug", "Item " + item.name + " is a folder." )
                            smil_file = SmilParse(item)
                            file_list = smil_file.smil_dereference()
                            item.destination = ("//" + target['Name'] + target['Path'] + 
                                           file_stub + "/")
                            log2log("info", "Copying folder " + source_folder + " to " + 
                                    item.destination)
                            for file in file_list:
                                statinfo = os.stat(file)
                                filename = os.path.basename(file)
                                csv_string += ("Started, " + 
                                    item.start_time.strftime("%Y-%m-%d") + "," +
                                    item.start_time.strftime("%H:%M:%S") + "," +
                                    socket.gethostname() + "," + file_stub + "," + 
                                    filename + "," + str(statinfo.st_size) + "," + 
                                    target['Name'] + "\n")                                
                        else:
                            # Single file copy setup
                            log2log('debug', "Item " + item.name + " is a file object.")
                            item.destination = ("//" + target['Name'] + target['Path'])                        
                        
                        # Add csv entry to the csv log queue
                        csv_log_queue.put(csv_string)
                        
                        # Add work to the copy queue
                        _task_queue.put(item)
                        
                    else:
                        log2log('info', "No empty targets were found for " + item.name + ".")
                        work_queue.put(item)                        
                        sleep(5)                    
                        
                except Exception as ex:
                    log2log('error', "Task Loading Exception:  " + str(ex))
                    log2log('error', traceback.format_exc())
                
                # Add new process if needed
                process_list = active_children()
                num_of_processes = ServiceConf().concurrent_copies
                while (_task_queue.qsize() > 0 and len(process_list) < (num_of_processes)):
                    p = Process(target=_worker, args=(_task_queue, _done_queue))
                    p.start()                    
                    process_list = active_children()
                    log2log('debug', "Process count = " + str(len(process_list)))
                    
                if (len(process_list) == 0 and _task_queue.qsize() == 0):
                    log2log("debug", "Zeroing out the target counts.")
                    self._zero_target_dict()
            else:
                # Wait until work is available
                sleep(10)
            
            # Process Post Copy Queue
            while (_done_queue.qsize() > 0):
                item = _done_queue.get()
                self.target_count[item.target['Name']] -= 1
                item.finish_time = datetime.datetime.now()
                post_copy_thread.post_work_queue.put(item)
                log2log("debug", "Get Target Counts: " + str(self.target_count))
                log2log("info", "Adding " + item.name + " to the post copy queue.")