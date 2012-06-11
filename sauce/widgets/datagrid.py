'''
Created on 29.05.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.forms as twf
import tw2.jquery as twj

from sprox.widgets import SproxDataGrid

tablesorter_js = twc.JSLink(
    #filename='static/javascript/jquery.tablesorter.js',
    link='/javascript/jquery.tablesorter.js',
    resources=[twj.jquery_js],
    location='headbottom')
tablesorter_css = twc.CSSLink(
    #filename='static/style/tablesorter.css',
    link='/css/tablesorter.css')


class JSSortableDataGrid(SproxDataGrid):
    resources = [tablesorter_js, tablesorter_css]
    css_class = 'tablesorter table table-striped table-condensed'

    headers = twc.Param(
        '',
        default={})
    sortList = twc.Param(
        '',
        default=[])

    def prepare(self):
        super(JSSortableDataGrid, self).prepare()
        if 'id' in self.attrs:
            selector = "#" + self.attrs['id'].replace(':', '\\:')
        else:
            selector = '.tablesorter'
        self.add_call(twj.jQuery(selector).tablesorter(dict(headers=self.headers,
            sortList=self.sortList)))
        