'''
Created on Nov 16, 2013

@author: moschlar
'''

import tw2.core.testbase as tb
from tw2.core.validation import ValidationError

from sauce.widgets.validators import FloatValidator, UniqueValidator
from sauce.model import User, DBSession
from sauce.tests import setup_db, teardown_db


# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()
    DBSession.add(User(id=4771, user_name='dummy', email_address='dummy@sauce.org'))
    DBSession.flush()


# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()


class TestFloatValidator(tb.ValidatorTest):
    validator = FloatValidator

    to_python_attrs = [{}, {}, {}]
    to_python_params = ['1', '0.1', 'asdf']
    to_python_expected = [1.0, 0.1, ValidationError]

    attrs = [{'required': False}, {'required': True}, {'min': 1.0}, {'max': 1.0}]
    params = ['', '', '0.9', '1.1']
    expected = [None, ValidationError, ValidationError, ValidationError]

    from_python_attrs = [{}, {}]
    from_python_params = [1.0, 0.1]
    from_python_expected = ['1.0', '0.1']


class TestUniqueValidator(tb.ValidatorTest):
    validator = UniqueValidator

    attrs = [{'entity': User, 'key': 'id'}, {'entity': User, 'key': 'id'},
        {'entity': User, 'key': 'id', 'allowed_values': '4711'}]
    params = ['1337', '4711', '4711']
    expected = ['1337', ValidationError, '4711']
