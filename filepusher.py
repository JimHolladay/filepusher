#------------------------------------------------------------------------------
# This is the main runner for FilePusher.
#     for use with python 3.5
#------------------------------------------------------------------------------
import time
import sys
import datetime
from pre_copy_thread import ImportValidationThread
from copy_thread import ProducerThread
from post_copy_thread import PostProducerThread
from config.log_settings import log2log
from csvlogger import csv_log_queue, CSVLogThread

if __name__ == "__main__":
    try:
        # create each thread for all the processes
        thread1 = ImportValidationThread(name='validation')
        thread2 = ProducerThread(name='producer')
        thread3 = PostProducerThread(name='postproducer')
        thread4 = CSVLogThread(name='csvlog')
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        while True:
            print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M') + 
                  " Still Working")
            time.sleep(600)
            
    except KeyboardInterrupt:
        sys.exit()
        
    except Exception as ex:
        log2log("error", "Main Exception... " + str(ex))
        log2log("error", str(sys.exc_info()))
        
    
