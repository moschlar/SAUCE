'''
Created on Nov 16, 2013

@author: moschlar
'''

import tw2.core.testbase as tb
from tw2.core.validation import ValidationError

from sauce.widgets.lib import FloatValidator, UniqueValidator
from sauce.model import User, DBSession
from sauce.tests import setup_db, teardown_db

# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()


# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()


class TestFloatValidator(tb.ValidatorTest):
    validator = FloatValidator

    to_python_attrs =    [{}, {}, {}]
    to_python_params =   ['1', '0.1', 'asdf']
    to_python_expected = [1.0, 0.1, ValidationError]

    attrs = [{'required': False}, {'required': True}]
    params = ['', '']
    expected = [None, ValidationError]

    from_python_attrs = [{}, {}]
    from_python_params = [1.0, 0.1]
    from_python_expected = ['1.0', '0.1']


class TestUniqueValidator(tb.ValidatorTest):
    validator = UniqueValidator

    attrs = [{'entity': User, 'key': 'id'}, {'entity': User, 'key': 'id'}]
    params = ['1337', '4711']
    expected = ['1337', ValidationError]

    def setUp(self):
        DBSession.add(User(id=4771, user_name='dummy'))
        DBSession.flush()
