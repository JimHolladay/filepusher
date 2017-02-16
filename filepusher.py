# ------------------------------------------------------------------------------
# This is the main runner for FilePusher.
#     for use with python 3.5
# ------------------------------------------------------------------------------
""" This is the main runner of Filepusher."""
import time
import sys
import datetime

from .pre_copy_thread import ImportValidationThread
from .copy_thread import ProducerThread
from .post_copy_thread import PostProducerThread
from .configuration.log_settings import log2log
from .csvlogger import CSVLogThread

if __name__ == "__main__":
    try:
        # create each thread for all the processes
        THREAD1 = ImportValidationThread(name='validation')
        THREAD2 = ProducerThread(name='producer')
        THREAD3 = PostProducerThread(name='post_producer')
        THREAD4 = CSVLogThread(name='csv_log')
        THREAD1.start()
        THREAD2.start()
        THREAD3.start()
        THREAD4.start()

        while True:
            print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M') +
                  " Still Working")
            time.sleep(600)

    except KeyboardInterrupt:
        sys.exit()

    except Exception as ex:
        log2log("error", "Main Exception... " + str(ex))
        log2log("error", str(sys.exc_info()))
