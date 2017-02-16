# ===============================================================================
# post_copy_thread.py for FilePusher
#
# This holds the queue and the process that happens after the copy process.
#
# for use with python 3.5
# ===============================================================================
""" This module contains the post copy thread and its logic."""
import time
import shutil as su
import os
import socket

from multiprocessing import Queue
from threading import Thread

from .copy_thread import _WORK_QUEUE
from .xml_parse.smil_file_parser import SmilParse
from .configuration.log_settings import log2log
from .file_and_folder import FolderObject
from .csvlogger import _CSV_LOG_QUEUE

_POST_WORK_QUEUE = Queue(100)


class PostProducerThread(Thread):
    """ This class does the post copy work on the post_work_queue. """
    def __init__(self, target=None, name=None):
        super(PostProducerThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not _POST_WORK_QUEUE.empty():
                item = _POST_WORK_QUEUE.get()
                log2log("debug", 'Post Producer Popped ' + item.name)
                source_folder = os.path.dirname(item.full_path)
                file_stub = item.name.split('-')[0]

                log2log("debug", "Testing post item: " + str(item.target))

                if item.isinstance(object, FolderObject):
                    smil_check = SmilParse(item)
                    print("Validating " + item.name + "...")
                    if smil_check.smil_probe():
                        log2log("debug", "Smil check passed. Deleting temp folder: " +
                                os.path.dirname(item.full_path))
                        su.rmtree(os.path.dirname(item.full_path))

                        # Write entries to the csv log
                        file_list = smil_check.smil_dereference()
                        stat_info = os.stat(item.destination + item.name)
                        finish_time = item.finish_time.strftime("%Y-%m-%d") + " " + \
                            item.finish_time.strftime("%H:%M:%S")
                        csv_dict = {'process_status': "Finished",
                                    'object_type': 'folder',
                                    'finish_time': finish_time,
                                    'source_machine': socket.gethostname(),
                                    'source_folder': source_folder,
                                    'item_name': file_stub,
                                    'object_size': str(stat_info.st_size),
                                    'target_name': item.target['Name']}
                        _CSV_LOG_QUEUE.put(csv_dict)
                        for file in file_list:
                            stat_info = os.stat(file)
                            csv_dict = {'process_status': "Finished",
                                        'object_type': 'folder_file',
                                        'finish_time': finish_time,
                                        'source_machine': socket.gethostname(),
                                        'source_folder': file_stub,
                                        'item_name': os.path.basename(file),
                                        'object_size': str(stat_info.st_size),
                                        'target_name': item.target['Name']}
                            _CSV_LOG_QUEUE.put(csv_dict)
                        print(item.name + " is finished moving.")
                    else:
                        # Copy Validation failed.
                        log2log("debug", "Smil check failed. Sending back to the copy queue.")
                        _WORK_QUEUE.put(item)
                else:
                    # Single file copy cleanup
                    if os.path.isfile(item.destination + item.name):
                        stat_info = os.stat(item.destination + item.name)
                        os.remove(source_folder + "\\" + item.name)
                        print(item.name + " is finished.")
                        csv_dict = {'process_status': "Finished",
                                    'object_type': 'single_file',
                                    'source_folder': source_folder,
                                    'source_machine': socket.gethostname(),
                                    'item_name': item.name,
                                    'object_size': stat_info.st_size,
                                    'target_name': item.target['Name'],
                                    'finish_time': item.finish_time}
                        _CSV_LOG_QUEUE.put(csv_dict)
                    else:
                        # file copy failed
                        log2log("debug", "File copy failed. Sending back to the copy queue.")
                        _WORK_QUEUE.put(item)
            else:
                time.sleep(1)
