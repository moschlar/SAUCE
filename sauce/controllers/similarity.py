# -*- coding: utf-8 -*-
"""Similarity controller module

TODO: Cache all_pairs result
"""

import logging
from difflib import SequenceMatcher

import matplotlib
matplotlib.use('Agg')  # Only backend available in server environments
import pylab
from ripoff import all_pairs, dendrogram

# turbogears imports
from tg import expose, abort, flash, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import Any, has_permission
from pygmentize import Pygmentize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import Assignment, Submission
from sauce.lib.helpers import udiff
from sauce.lib.auth import has_teacher, has_teachers
from sauce.lib.menu import menu
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

log = logging.getLogger(__name__)


class SimilarityController(BaseController):

    def __init__(self, assignment):
        self.assignment = assignment
        self.submissions = sorted((s for s in self.assignment.submissions if s.source), key=lambda s: s.id)

        self.allow_only = Any(has_teacher(self.assignment),
                              has_teacher(self.assignment.sheet),
                              has_teacher(self.assignment.sheet.event),
                              has_teachers(self.assignment.sheet.event),
                              has_permission('manage'),
                              msg=u'You are not allowed to access this page.'
                              )

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.assignment)

#    @expose('sauce.templates.page')
#    def index(self):
#        return dict(heading='Similarity stuff', content=u'''
#<ul>
#  <li><a href="/similarity/similarity">Similarity table</a></li>
#  <li><a href="/similarity/dendrogram">Similarity dendrogram</a></li>
#  <li><a href="/similarity/graph_force">Force-directed graph</a>
#    <ul>
#      <li><a href="/similarity/data_nodes">Plain data (hand-made)</a></li>
#      <li><a href="/similarity/data_nx">Plain data (networkx-made)</a></li>
#    </ul>
#  </li>
#  <li><a href="/similarity/graph_chord">Chord diagram</a>
#    <ul>
#      <li><a href="/similarity/data_matrix">Plain data (hand-made)</a></li>
#    </ul>
#  </li>
#</ul>''')

    def get_similarity(self):
        matrix = all_pairs([s.source or u'' for s in self.submissions])
        return matrix

    @expose('sauce.templates.similarity')
    def index(self, cmap_name='RdYlGn', *args, **kw):
        def rgb(v):
            '''Get CSS rgb representation from color map with name'''
            cmap = pylab.get_cmap(cmap_name)
            (r, g, b, _) = cmap(v)
            return 'rgb(' + ','.join('%d' % int(x * 255) for x in (r, g, b)) + ')'
        c.rgb = rgb
        c.url = self.assignment.url + '/similarity'
        matrix = self.get_similarity()
        return dict(page='assignment', assignment=self.assignment, matrix=matrix,
            submissions=self.submissions)

    @expose(content_type="image/png")
    def dendrogram(self):
        return dendrogram(self.get_similarity(),
            leaf_label_func=lambda i: unicode(self.submissions[i].id),
            leaf_rotation=45)

    @expose()
    def diff(self, *args, **kw):
        try:
            a = Submission.query.filter_by(id=int(args[0])).one()
            b = Submission.query.filter_by(id=int(args[1])).one()
        except ValueError:
            abort(400)
        except IndexError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            log.warn('', exc_info=True)
            abort(500)
        else:
            pyg = Pygmentize(full=True, linenos=False,
                title='Submissions %d and %d, Similarity: %.2f' % (a.id, b.id,
                    SequenceMatcher(a=a.source or u'', b=b.source or u'').ratio()))
            return pyg.display(lexer='diff',
                source=udiff(a.source, b.source, unicode(a), unicode(b)))
