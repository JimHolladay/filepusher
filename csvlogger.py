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

from .config.log_settings import log2log

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
                        line = dictionary['process_status'] + ", " + \
                            dictionary['source_folder'] + ", " + \
                            dictionary['item_name'] + ", " + \
                            dictionary['object_size'] + ", " + \
                            dictionary['target_name'] + ", " + \
                            dictionary['finish_time']
                        csv_file.write(line)
                        sleep(1)
            except Exception as ex:
                log2log('debug', "CSV Log exception " + str(ex))
                log2log('debug', traceback.format_exc())


source_folder, item.name, statinfo.st_size, item.target['Name'], item.finish_time

csv_dict = {'process_status': "Finished",
            'source_folder': source_folder,
            'item_name': item.name,
            'object_size': statinfo.st_size,
            'target_name': item.target['Name'],
            'finish_time': item.finish_time}