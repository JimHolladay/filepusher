# ===============================================================================
# pre_copy_thread.py for FilePusher
#
# This holds the queue and the process that operate on the files acquired by the
# watch folder.  This file handles the processes before the copy.
#
# for use with python 3.5
# ===============================================================================
""" This is the validation thread that handles the processes. """
import time
import re
import os

import shutil as su
import traceback
from multiprocessing import Queue
from threading import Thread

from .copy_thread import _WORK_QUEUE
from .xml_parse.smil_file_parser import SmilParse
<<<<<<< HEAD
from .configuration.config_service import ServiceConf
from .configuration.log_settings import log2log
=======
from .config.config_ingest_service import ServiceConf
from .config.log_settings import log2log
>>>>>>> 4b408d7375164af2d19e9c52586cd24fa16192c8
from .file_and_folder import FolderObject, FileObject

_IMPORT_QUEUE = Queue(200)


class ImportValidationThread(Thread):
    """ This class ingests the items from the import queue. """
    def __init__(self, target=None, name=None):
        super(ImportValidationThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            try:
                conf_service = ServiceConf()
                for product in conf_service.product_list:
                    for file in os.scandir(str(product['WatchPath'])):
                        if str(r"*" + os.path.splitext(file.name)[1]) == \
                                str(product['WatchPattern']):
                            file_stub = str(file.name).split('-')[0]
                            file_path = os.path.dirname(file.path)
                            temp_file_dest = conf_service.temp_move_path + file_stub

                            log2log('debug', "File stub: " + file_stub)
                            log2log('debug', "File path: " + file_path)
                            log2log('debug', "temp file dest: " + temp_file_dest)

                            if not bool(product['SingleFiles']) and \
                                    bool(product['ValidateViaSmil']):
                                log2log('debug', "made it to smil check.")
                                temp_check = FolderObject(file.name, file.path)
                                smil_check = SmilParse(temp_check)
                                if smil_check.smil_probe():
                                    log2log('debug', "Smil check passed.")

                                    # move the files to the temp folder
                                    if os.path.exists(temp_file_dest):
                                        su.rmtree(temp_file_dest, ignore_errors=True)
                                    os.mkdir(temp_file_dest)
                                    for stream_file in smil_check.smil_dereference():
                                        filename = os.path.basename(stream_file)
                                        log2log('debug', "Move check: " +
                                                file_path + "\\" + filename)
                                        su.move(file_path + "\\" + filename,
                                                temp_file_dest + "\\" + filename)
                                    su.move(file_path + "/" + file.name,
                                            temp_file_dest + "/" + file.name)
                                    log2log("info", "Adding " + file.name +
                                            " to the work queue.")
                                    print("Adding " + file.name +
                                          " to the work queue.")
                                    temp_entry = FolderObject(file.name,
                                                              temp_file_dest +
                                                              "/" + file.name)
                                    _WORK_QUEUE.put(temp_entry)

                            elif bool(product['SingleFiles']):
                                regex = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]+-[0-9]' + \
                                        '{3,4}_[0-9]{3,4}x[0-9]{3,4}.mp4$'
                                if re.search(regex, file.name):
                                    su.move(file_path + "/" + file.name, temp_file_dest)
                                    log2log("debug", "Adding " + file.name +
                                            " to the copy queue.")
                                    print("Adding " + file.name + " to the copy queue.")
                                    _WORK_QUEUE.put(FileObject(file.name, file.path))
                                else:
                                    log2log("error", file.name + " has an invalid filename.")
                    log2log('debug', "Time to sleep.")
                    time.sleep(15)
            except Exception as ex:
                log2log('error', "Queue creator exception: " + str(ex))
                log2log('error', traceback.format_exc())
