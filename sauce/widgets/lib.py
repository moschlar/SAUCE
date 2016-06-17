# -*- coding: utf-8 -*-
'''Auxiliary stuff for SAUCE widgets

@since: 2015-01-07
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
import tw2.jquery as twj


ays_js = twc.JSLink(
    link='/javascript/jquery.are-you-sure.js',
    resources=[twj.jquery_js],
    location='headbottom',
)


def make_ays_init(**kwargs):
    return twj.jQuery(twc.js_symbol('document')).ready(twc.js_symbol(u'''\
function () {
    $("%(form)s").areYouSure();
}''' % kwargs))


# TODO: Are-you-sure hook for Wysihtml5


def make_cm_changes_save(**kwargs):
    return twj.jQuery(twc.js_symbol('document')).ready(twc.js_symbol(u'''\
function () {
    $("%(selector)s + .CodeMirror")[0].CodeMirror.on('changes', function(instance) { instance.save(); });
}''' % kwargs))


def make_cm_line_number_update_func(**kwargs):
    return twj.jQuery(twc.js_symbol('document')).ready(twc.js_symbol(u'''\
function () {
    var cm_head = $("%(scaffold_head)s + .CodeMirror")[0].CodeMirror;
    var cm_source = $("%(source)s + .CodeMirror")[0].CodeMirror;
    var cm_foot = $("%(scaffold_foot)s + .CodeMirror")[0].CodeMirror;

    var cm_head_cnt = cm_head.getDoc().lineCount();
    var cm_source_doc = cm_source.getDoc();

    function updateFootFirstLineNumber(instance, changeObj) {
        var lines = cm_head_cnt + cm_source_doc.lineCount() + 1;
        cm_foot.setOption('firstLineNumber', lines);
    }

    // Initially set firstLineNumber for source
    cm_source.setOption('firstLineNumber', cm_head_cnt + 1);

    // Initially set firstLineNumber for scaffold_foot
    updateFootFirstLineNumber();

    cm_source.on('changes', updateFootFirstLineNumber);
}''' % kwargs))


def make_cm_readonly_lines_func(value, **kwargs):
    '''

    :type value: sauce.model.submission.Submission
    '''

    func = u'''\
function () {
    var cm = $("%(selector)s + .CodeMirror")[0].CodeMirror;
'''
    cond = []
    start_head, end_head, start_foot, end_foot = value.scaffold_line_numbers
    if value.scaffold_head:
        kwargs['readOnlyHeadStart'] = start_head
        kwargs['readOnlyHeadEnd'] = end_head
        func += '''\
    cm.markText({line: %(readOnlyHeadStart)d, ch: 0}, {line: %(readOnlyHeadEnd)d, ch: 0}, {readOnly: true, atomic: true, inclusiveLeft: true});
'''
        cond.append('(lineInfo.line < %(readOnlyHeadEnd)d)' % kwargs)
    if value.scaffold_foot:
        kwargs['readOnlyFootStart'] = start_foot
        kwargs['readOnlyFootEnd'] = end_foot
        func += '''\
    cm.markText({line: %(readOnlyFootStart)d - 1, ch: undefined}, {line: %(readOnlyFootEnd)d, ch: undefined}, {readOnly: true, atomic: true, inclusiveRight: true});
'''
        cond.append('(lineInfo.line >= %(readOnlyFootStart)d)' % kwargs)
    if cond:
        func += '''\
    cm.eachLine(function(line) {
        var lineInfo = cm.lineInfo(line);
        if (%(cond)s) {
            cm.addLineClass(line, 'wrap', 'readOnly');
        }
    });
'''
        kwargs['cond'] = '||'.join(cond)
    func += '''\
}
'''
    return twj.jQuery(twc.js_symbol('document')).ready(twc.js_symbol(func % kwargs))
