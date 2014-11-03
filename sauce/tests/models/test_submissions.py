'''
Created on Mar 12, 2014

@author: moschlar
'''

import unittest

from sauce.model import Assignment, Submission


class TestSubmission(unittest.TestCase):

    def test_submission_full_source(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD',
            submission_scaffold_foot=u'FOOT',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY',
        )
        assert s.full_source == u'HEAD\nBODY\nFOOT\n', s.full_source
