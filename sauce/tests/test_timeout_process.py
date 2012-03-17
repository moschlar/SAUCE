'''
Created on 15.03.2012

@author: moschlar
'''
from unittest import TestCase
from sauce.tests import *

#from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, Student, DBSession as Session
#import transaction
from sauce.lib.runner import TimeoutProcess

# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()

# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()

class TestTimeoutProcess(TestCase):
    '''Test the timeout-aware process runner'''
    
    def setUp(self):
        '''Set up TimeoutProcess object'''
        
        self.timeoutProcess = TimeoutProcess()
    
    def test_ok(self):
        '''Test a program that returns quickly'''
        
        argv = ['/bin/date']
        timeout = 1
        t = self.timeoutProcess(argv, timeout)
        # If process finished before timeout, it should return 0
        self.assertEqual(t.returncode, 0, "%s ran into %d second timeout..." % (" ".join(argv), timeout))
    
    def test_fail(self):
        '''Test a program that does not return quickly'''
        
        argv = ['/bin/sleep', '2']
        timeout = 1
        t = self.timeoutProcess(argv, timeout)
        # If process does not finish before timeout, it returns -15
        self.assertNotEqual(t.returncode, 0, "%s did not run into %d second timeout..." % (" ".join(argv), timeout))
