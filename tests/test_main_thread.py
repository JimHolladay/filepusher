'''
This will test all assests of the main_thread file in the main folder.

'''

from main_thread import ImportValidationThread, ProducerThread, PostProducerThread
from main_thread import import_queue, work_queue, post_work_queue
import unittest

class TestThreads(unittest.TestCase):
    pass
    
class TestQueues(unittest.TestCase):
    
    def test_import_queue_will_take_value(self):
        '''Test that the import_queue will take a value'''
        strValue = "testes"
        import_queue.put(strValue)
        self.assertEqual(import_queue.get(), strValue, msg = None)
    
    def test_import_queue_is_empty(self):
        self.assertTrue(import_queue.empty())
        
    def test_work_queue_will_take_value(self):
        '''Test that the work_queue will take a value'''
        strValue = "testes"
        work_queue.put(strValue)
        self.assertEqual(work_queue.get(), strValue, msg = None)
    
    def test_work_queue_is_empty(self):
        self.assertTrue(work_queue.empty())
        
    def test_post_work_queue_will_take_value(self):
        '''Test that the post_work_queue will take a value'''
        strValue = "testes"
        post_work_queue.put(strValue)
        self.assertEqual(post_work_queue.get(), strValue, msg = None)

    def test_post_work_queue_is_empty(self):
        self.assertTrue(post_work_queue.empty())
        
if __name__ == "__main__":
    unittest.main()

