# -*- coding: utf-8 -*-
'''JSSortableDataGrid

@see: :mod:`tw2.core`
@see: :mod:`sprox`

@since: 29.05.2012
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
