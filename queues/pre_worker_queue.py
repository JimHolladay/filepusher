# =======================================================================
# pre_worker_queue.py
#
#   This module contains the queue and the overloaded modules for
# validation work before the main worker.
#
# ========================================================================
""" This is the prework queue. """

from multiprocessing import Queue

_IMPORT_QUEUE = Queue(200)
