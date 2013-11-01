'''
@since: 29.10.2013

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from sqlalchemy.orm.util import class_mapper

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from nose.tools import eq_

from sauce.model import Assignment, Test, DBSession
import transaction

from sauce.tests import setup_db, teardown_db


__all__ = ['TestTest']


# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()
    assignment = Assignment(id=42, name='Dummy', assignment_id=42)
    DBSession.add(assignment)
    transaction.commit()


# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()

DEFAULT = object()

matrix = [
    # kwargs, expected_output_data, good_output_data, bad_output_data

    (dict(ignore_case=True),
        'HELLO',
        ['HELLO', 'hello']
    ),
    (dict(ignore_case=False),
        'HELLO',
        ['HELLO'],
        ['hello']
    ),

    (dict(),
        'HELLO',
        ['#HELLO\nHELLO'],
        ['hello\nHELLO']
    ),
    (dict(comment_prefix=None),
        '#HELLO',
        ['#HELLO']
    ),
    (dict(comment_prefix='//'),
        'HELLO',
        ['//hello\nHELLO'],
        ['hello\nHELLO']
    ),

    (dict(),
        '1 2 3',
        ['1 2 3', '1\t2\n3\n'],
        ['1,2,3']
    ),
    (dict(separator=' '),
        '1 2 3',
        ['1 2 3'],
        ['1,2,3', '1\t2\n3\n']
    ),
    (dict(separator=','),
        '1,2,3',
        ['1,2,3'],
        ['1 2 3', '1\t2\n3\n']
    ),

    (dict(splitlines=False, split=False),
        '1\n2\n3\n4 5 6',
        ['1\n2\n3\n4 5 6']
    ),
    (dict(splitlines=True, split=False),
        '1\n2\n3\n',
        ['1\n2\n3\n', '1\n2\n3'],
        ['1 2 3', '1\t2\n3\n', '1,2,3']
    ),
    (dict(splitlines=True, split=True),
        '1 2 3\n4 5 6\n',
        ['1 2 3\n4 5 6', '1\t2\t3\n4\t5\t6\n'],
        ['1 2 3 4 5 6']
    ),
    (dict(splitlines=True, split=True, separator=','),
        '1,2,3\n4,5,6\n',
        ['1,2,3\n4,5,6'],
        ['1 2 3 4 5 6']
    ),

    (dict(split=True, sort=True),
        '1\n2\n3\n',
        ['1\n2\n3\n', '3 2 1'],
        ['1 1 2']
    ),
    (dict(splitlines=True, split=True, sort=True),
        '1 2 3\n4 5 6\n',
        ['1 2 3\n4 5 6', '1\t2\t3\n6\t5\t4\n'],
        ['1 2 3 4 5 6']
    ),
    (dict(split=True, sort=True),
        '1\n2\n3\n',
        ['1\n2\n3\n', '3 2 1'],
        ['1 1 2']
    ),

    (dict(parallel_sort=True),
        'a [1]\nb [2]\nc [3]\n',
        ['a [1]\nb [2]\nc [3]\n', 'a [1]\nc [3]\nb [2]\n'],
        ['a [1]\nb [2]\nd [4]\n']
    ),
    (dict(parallel_sort=True),
        'x\ny\nz\naa [1]\nab [1]\nb [2]\nca [3]\ncb [3]\n',
        ['x\naa [1]\ny\nca [3]\nb [2]\nab [1]\nz\ncb [3]\n'],
    ),
]


def _test_attr(args):
    kwargs, expected_output_data, good_output_data = args[0:3]
    bad_output_data = args[4:]
    test = Test(assignment_id=42, output_data=expected_output_data, **kwargs)
    DBSession.add(test)
    transaction.commit()
    test = DBSession.merge(test)

    print kwargs, test.separator, test.split, test.splitlines

    for d in good_output_data:
        result, _, expected, output, _ = test.validate(d)
        print '_'
        converted_output = test.unconvert(test.convert(d))
        assert result is True, (expected, output, converted_output)
    for d in bad_output_data:
        result, _, expected, output, _ = test.validate(d)
        converted_output = test.unconvert(test.convert(d))
        assert result is False, (expected, output, converted_output)


def test_matrix():
    for row in matrix:
        yield (_test_attr, row)


class TestTest(TestCase):
    '''Test the Test conversion options'''

    def test_show_partial_match(self):
        test = Test(
            output_data=u'Hello World',
            show_partial_match=True,
        )
        self.assertTupleEqual(test.validate('Hello')[0:2], (False, True))
        self.assertTupleEqual(test.validate('Hello World')[0:2], (True, False))

    def test_no_show_partial_match(self):
        test = Test(
            output_data=u'Hello World',
            show_partial_match=False,
        )
        self.assertTupleEqual(test.validate('Hello')[0:2], (False, False))
        self.assertTupleEqual(test.validate('Hello World')[0:2], (True, False))
