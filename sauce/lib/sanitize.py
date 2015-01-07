# -*- coding: utf-8 -*-
"""HTML sanitizing tools

The rule sets are taken from Wysihtml5.
This file can be used as a script to convert a Wysihtml5 parser rules
file to a proper Python representation for using it with bleach.

@since: 2015-01-07
@author: moschlar
"""

from bleach import clean
from functools import partial


rulesets = {
    'basic': {
        'tags': ['br', 'span', 'div', 'p'],
        'strip': True,
    },
    'simple': {
        'tags': [u'em', u'a', u'b', u'span', u'p', u'i', u'li', u'ul', u'ol', u'br', u'div', u'strong'],
        'attributes': {u'a': [u'href', u'target', u'rel']},
        'strip': True,
    },
    'advanced': {
        'tags': [u'em', u'pre', u'code', u'h2', u'h3', u'h1', u'h6', u'h4', u'h5', u'table', u'strong', u'span', u'img', u'ul', u'tr', u'tbody', u'li', u'tfoot', u'th', u'td', u'cite', u'thead', u'blockquote', u'hr', u'b', u'br', u'caption', u'a', u'ol', u'i', u'q', u'p', u'u', u'div'],
        'attributes': {u'a': [u'href', u'target', u'rel'], u'blockquote': [u'cite'], u'img': [u'width', u'alt', u'src', u'height'], u'q': [u'cite'], u'th': [u'colspan', u'rowspan'], u'td': [u'colspan', u'rowspan']},
        'strip': True,
    },
}


def bleach(text, ruleset, **kwargs):
    ruleset = rulesets[ruleset].copy()
    ruleset.update(kwargs)
    return clean(text, **ruleset)


bleach_basic = partial(bleach, ruleset='basic')
bleach_simple = partial(bleach, ruleset='simple')
bleach_advanced = partial(bleach, ruleset='advanced')


#----------------------------------------------------------------------


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
