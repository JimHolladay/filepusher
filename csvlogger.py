# ===============================================================================
# csvlogger.py for FilePusher
#
# This holds the queue and the process to write to the csv file.
#
# for use with python 3.5
# ===============================================================================
""" This module holds the thread for adding items to the csv log."""
import datetime
import traceback

from time import sleep
from multiprocessing import Queue
from threading import Thread

<<<<<<< HEAD
from .configuration.log_settings import log2log
=======
from .config.log_settings import log2log
>>>>>>> 4b408d7375164af2d19e9c52586cd24fa16192c8

_CSV_LOG_QUEUE = Queue(100)


class CSVLogThread(Thread):
    """ This class writes to the CSV file. """
    def __init__(self, name=None):
        super(CSVLogThread, self).__init__()
        self.name = name

    def run(self):
        while True:
            try:
                if not _CSV_LOG_QUEUE.empty():
                    date_name = datetime.date.today().strftime('%Y-%m-%d')
                    with open("z:/Archive/" + self.name + "_" + date_name + ".csv", 'a') \
                            as csv_file:
                        dictionary = _CSV_LOG_QUEUE.get()
                        line = _string_builder(dictionary)
                        csv_file.write(line)
                        sleep(1)
            except Exception as ex:
                log2log('debug', "CSV Log exception " + str(ex))
                log2log('debug', traceback.format_exc())


def _string_builder(dictionary=None):
    """ Builds the string to print to the csv file. """
    line = (dictionary['process_status'] + ", " +
            dictionary['source_machine'] + ", " +
            dictionary['source_folder'] + ", " +
            dictionary['item_name'] + ", " +
            dictionary['object_type'] + ", " +
            dictionary['object_size'] + ", " +
            dictionary['target_name'] + ", " +
            dictionary['finish_time'])
    return line
