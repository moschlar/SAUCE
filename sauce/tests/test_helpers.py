'''
Created on 23.03.2012

@author: moschlar
'''
from unittest import TestCase
from datetime import timedelta

from sauce.lib.helpers import strftimedelta, striphtml, cut

__all__ = ['TestHelpers']


class TestHelpers(TestCase):

    def test_strftimedelta(self):
        
        t = timedelta(days=2, hours=25)
        self.assertEqual(strftimedelta(t), '3 days and 1 hour')
        
        t = timedelta(days=1, hours=15, minutes=9, seconds=34)
        self.assertEqual(strftimedelta(t), '1 day, 15 hours and 9 minutes')
    
    def test_striphtml(self):
        
        self.assertEqual(striphtml('<p>Paragraph</p>'), 'Paragraph')
        
        self.assertEqual(striphtml('<div class="bla">Some<br />weird &lt; Stuff</div>'), 'Some weird &lt; Stuff')
    
    def test_cut(self):
        
        self.assertEqual(cut('Short Text'), 'Short Text')
        
        long = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'
        long_300 = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo...'
        self.assertEqual(cut(long), long_300)
        