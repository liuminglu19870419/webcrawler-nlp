'''

@author: mingliu
'''
import unittest
from rabbitmq_select_client import Select_Connnection
import time
import threading


class Test(unittest.TestCase):
    
    def process(self, message, body):
        print message, body

    def setUp(self):
        self.select_connection = Select_Connnection(process_handler=self.process)
        pass


    def tearDown(self):
        pass


    def testStart(self):
        
        pass
    
    def fun(self):
        message_key = 'test_message'
        for i in range(2000000):
            print i
            now = int(time.time())
            msg = {
                'id': now % (i + 1),
                'name': 'producer %s' % (now % 10),
                'phone': now,
                '__priority': (now % 3),
            }
            message = {'message_key': message_key,
                       'message_body': msg}
            self.select_connection.publish(message) 
            time.sleep(0.1)
        self.select_connection.stop()
    
    def testPublish(self):
        threading.Thread(target=self.fun).start()
        self.select_connection.start()
          
    def testStop(self):
#         self.select_connection.stop()
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()