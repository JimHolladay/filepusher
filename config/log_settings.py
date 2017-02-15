# ===============================================================================
# log_settings.py for FilePusher
#
# This is the class that controls the log config settings and ingest..
#
# for use with python 3.5
# ===============================================================================
""" This is the wrapper for the logger. """
import logging
import datetime


def log2log(log_type, msg):
    """ Wrapper for the logging module. """
    try:
        debug_log = logging.getLogger('full-log')
        log_file_name = 'Z:/Logs/filepusher/log-' + \
                        datetime.date.today().strftime('%Y-%m-%d') + \
                        ".txt"
        debug_log_handler = logging.handlers.RotatingFileHandler(filename=log_file_name,
                                                                 maxBytes=500000,
                                                                 backupCount=365,
                                                                 encoding='utf8')
        debug_log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        if not debug_log.hasHandlers():
            debug_log.addHandler(debug_log_handler)
        debug_log.setLevel(logging.DEBUG)
        if log_type == 'debug':
            debug_log.debug(msg)
        elif log_type == 'info':
            debug_log.info(msg)
        elif log_type == 'warning':
            debug_log.warning(msg)
        elif log_type == 'error':
            debug_log.error(msg)
        else:
            print("Error in log generation.")
        debug_log_handler.close()
        debug_log.removeHandler(debug_log_handler)
    except Exception as ex:
        print("Log2Log Exception happened: " + str(ex))

if __name__ == '__main__':
    log2log('debug', "This is just a test.")
