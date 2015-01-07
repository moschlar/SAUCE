# -*- coding: utf-8 -*-
'''Auxiliary validators for SAUCE widgets

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

from tg.i18n import ugettext as _
import tw2.core as twc
from sqlalchemy.orm.exc import NoResultFound
import bleach


try:
    _()
except TypeError:
    _ = lambda x: x


class FloatValidator(twc.validation.RangeValidator):
    """
    Confirm the value is an integer. This is derived from
    :class:`RangeValidator` so `min` and `max` can be specified.
    """
    msgs = {
        'notfloat': _('Must be a float'),
    }

    def to_python(self, value, state=None):
        value = super(FloatValidator, self).to_python(value, state)
        try:
            if value is None or unicode(value) == '':
                return None
            else:
                return float(value)
        except ValueError:
            raise twc.validation.ValidationError('notfloat', self)

    def _validate_python(self, value, state=None):
        if self.required and value is None:
            raise twc.validation.ValidationError('required', self)
        if value is not None:
            if self.min and value < self.min:
                raise twc.validation.ValidationError('toosmall', self)
            if self.max and value > self.max:
                raise twc.validation.ValidationError('toobig', self)

    def from_python(self, value, state=None):
        if value is None:
            return None
        else:
            return unicode(value)


class UniqueValidator(twc.Validator):

    msgs = {
        'notunique': _('Not unique'),
    }

    def __init__(self, entity, key, allowed_values=None, **kw):
        super(UniqueValidator, self).__init__(**kw)
        self.entity = entity
        self.key = key
        self.allowed_values = allowed_values or []

    def _validate_python(self, value, state=None):
        if value in self.allowed_values:
            return value
        try:
            self.entity.query.filter_by(**{self.key: value}).one()
        except NoResultFound:
            return value
        else:
            raise twc.ValidationError('notunique', self)


class BleachValidator(twc.StringLengthValidator):
    tags = None
    attributes = None
    styles = None
    strip_tags = True
    strip_comments = None

    def __init__(self, **kw):
        for attr in ('tags', 'attributes', 'styles', 'strip_tags', 'strip_comments'):
            if attr in kw and kw[attr] is not None:
                setattr(self, attr, kw.pop(attr))
        super(BleachValidator, self).__init__(**kw)

    def _convert_to_python(self, value, state=None):
        bleach_kwargs = {}
        for a in ('tags', 'attributes', 'styles', ('strip_tags', 'strip'), 'strip_comments'):
            if isinstance(a, tuple):
                a, b = a
            else:
                b = a
            if getattr(self, a, None) is not None:
                bleach_kwargs[b] = getattr(self, a)
        value = bleach.clean(value, **bleach_kwargs)
        return value


wysihtml5_basic_tags = ['br', 'span', 'div', 'p']
wysihtml5_basic = {'tags': wysihtml5_basic_tags}


class BasicWysihtml5BleachValidator(BleachValidator):
    tags = wysihtml5_basic_tags


wysihtml5_simple_tags = [u'em', u'a', u'b', u'span', u'p', u'i', u'li', u'ul', u'ol', u'br', u'div', u'strong']
wysihtml5_simple_attributes = {u'a': [u'href', u'target', u'rel']}
wysihtml5_simple = {'tags': wysihtml5_simple_tags, 'attributes': wysihtml5_simple_attributes}


class SimpleWysihtml5BleachValidator(BleachValidator):
    tags = wysihtml5_simple_tags
    attributes = wysihtml5_simple_attributes


wysihtml5_advanced_tags =  [u'em', u'pre', u'code', u'h2', u'h3', u'h1', u'h6', u'h4', u'h5', u'table', u'strong', u'span', u'img', u'ul', u'tr', u'tbody', u'li', u'tfoot', u'th', u'td', u'cite', u'thead', u'blockquote', u'hr', u'b', u'br', u'caption', u'a', u'ol', u'i', u'q', u'p', u'u', u'div']
wysihtml5_advanced_attributes = {u'a': [u'href', u'target', u'rel'], u'blockquote': [u'cite'], u'img': [u'width', u'alt', u'src', u'height'], u'q': [u'cite'], u'th': [u'colspan', u'rowspan'], u'td': [u'colspan', u'rowspan']}
wysihtml5_advanced = {'tags': wysihtml5_advanced_tags, 'attributes': wysihtml5_advanced_attributes}


class AdvancedWysihtml5BleachValidator(BleachValidator):
    tags = wysihtml5_advanced_tags
    attributes = wysihtml5_advanced_attributes


def _convert_wysihtml5_parser_rules(parser_rules_filename,
        parser_rules_varname='wysihtml5ParserRules'):
    """
    This is a small helper to extract the wysihtml5ParserRules variable
    from a wysihtml5 parser rules file and convert it to a representation
    suitable for bleach.
    """
    from collections import defaultdict

    try:
        import demjson
        from slimit.parser import Parser
        from slimit.visitors import nodevisitor
        from slimit import ast
    except ImportError:
        print 'You need to install the packages demjson and slimit for this to work...'
        raise

    with open(parser_rules_filename) as f:
        parser = Parser()
        tree = parser.parse(f.read())
        value = None
        for node in nodevisitor.visit(tree):
            if isinstance(node, ast.VarDecl) and node.identifier.value == parser_rules_varname:
                value = node.initializer
                break
        if not value:
            raise Exception
        # print value.to_ecma()

        obj = demjson.decode(value.to_ecma())
        # print obj

        tags = set()
        attributes = defaultdict(set)
        for tag, options in obj['tags'].items():
            if 'remove' not in options:
                if 'rename_tag' in options:
                    tag = options['rename_tag']
                if 'check_attributes' in options:
                    attributes[tag].update(options['check_attributes'].keys())
                if 'set_attributes' in options:
                    attributes[tag].update(options['set_attributes'].keys())
                tags.add(tag)

        tags = list(tags)
        attributes = dict((k, list(v)) for k,v in attributes.items())

        return tags, attributes

if __name__ == '__main__':
    import sys
    # from pprint import pprint

    tags, attributes = _convert_wysihtml5_parser_rules(sys.argv[1])

    print tags
    print attributes

    # pprint(tags)
    # pprint(attributes)
