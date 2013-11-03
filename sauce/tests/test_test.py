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

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from nose.tools import eq_

from sauce.model import Assignment, Test, DBSession

from sauce.tests import setup_db, teardown_db


__all__ = ['TestTest']


# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()
    assignment = Assignment(id=42, name='Dummy', assignment_id=42)
    DBSession.add(assignment)
    DBSession.flush()


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
        ['x\naa [1]\ny\nca [3]\nb [2]\nab [1]\nz\nca [3]\n'],
    ),

    (dict(parse_int=True),
        '1 2 3',
        ['1 2 3', '1   2   3'],
        ['1.0 2.0 3.0']
    ),
    (dict(parse_float=True),
        '1.0 2.0 3.0',
        ['1 2 3', '1   2   3', '1.0 2.0 3.0'],
        ['1.1 2.2 3.3']
    ),
    (dict(parse_float=True),
        '1.1 2.2 3.3',
        ['1.1 2.2 3.3', '1.10 2.20 3.30'],
        ['1.11 2.22 3.33']
    ),
    (dict(parse_float=True, float_precision=0),
        '1.0 2.0 3.0',
        ['1 2 3', '1.0 2.0 3.0', '1.1 2.2 3.3'],
        ['1.9 2.8 3.7']
    ),
    (dict(parse_float=True, float_precision=2),
        '1.00 2.00 3.00',
        ['1 2 3', '1.0 2.0 3.0'],
    ),
]


def _test_attr(args):
    kwargs, expected_output_data, good_output_data = args[0:3]
    bad_output_data = args[4:]
    test = Test(assignment_id=42, output_data=expected_output_data, **kwargs)
    DBSession.add(test)
    DBSession.flush()
    test = DBSession.merge(test)

    for d in good_output_data:
        result, _, expected, output, _ = test.validate(d)
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

    def test_integration_1(self):
        test = Test(
            assignment_id=42,
            output_data=u'1.0,2.0,3.0\n4.0,5.0,6.0\n7.0,8.0,9.0\n',
            separator=',', split=True, splitlines=True,
            parse_float=True, float_precision=1,
        )
        DBSession.add(test)
        DBSession.flush()
        test = DBSession.merge(test)
        d = u'#Result:\n1,2,3\n4,5,6\n,7,8,9\n'
        result, _, expected, output, _ = test.validate(d)
        converted_output = test.unconvert(test.convert(d))
        assert result is True, (expected, output, converted_output)

    def test_integration_2(self):
        test = Test(
            assignment_id=42,
            output_data=u'42 Bananas\n4711 Strawberrys\n1337 Apples\n',
            splitlines=True, split=False, sort=True,
        )
        DBSession.add(test)
        DBSession.flush()
        test = DBSession.merge(test)
        d = u'#Result:\n4711 Strawberrys\n42 Bananas\n1337 Apples\n'
        result, _, expected, output, _ = test.validate(d)
        converted_output = test.unconvert(test.convert(d))
        assert result is True, (expected, output, converted_output)
