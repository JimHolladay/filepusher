#===============================================================================
# csvlogger.py for FilePusher
# 
# This holds the queue and the process to write to the csv file.
#
# for use with python 3.5
#===============================================================================
import datetime
import traceback
from time import sleep
from multiprocessing import Queue
from threading import Thread
from config.log_settings import log2log
from config.log_settings import log2log

csv_log_queue = Queue(100)

class CSVLogThread(Thread):
    ''' This class writes to the CSV file. '''
    def __init__(self, group = None, target = None, name = None, args = (), 
                 kwargs = None, daemon = None):
        super(CSVLogThread, self).__init__()
    
    def run(self):
        while True:
            try:                
                if not csv_log_queue.empty():
                    datename = datetime.date.today().strftime('%Y-%m-%d')
                    with open("z:/Archive/" + datename + ".csv", 'a') as csvfile:
                        line = csv_log_queue.get()
                        csvfile.write(line)
                        sleep(1)
            except Exception as ex:
                log2log('debug', "CSV Log exception " + str(ex))
                log2log('debug', traceback.format_exc())