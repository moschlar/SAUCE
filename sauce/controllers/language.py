# -*- coding: utf-8 -*-
"""Language controller module"""
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

# turbogears imports
from tg import TGController, expose, flash, abort, tmpl_context as c

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
import status
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
#from sauce.lib.base import BaseController
from sauce.model import DBSession, Language

log = __import__('logging').getLogger(__name__)


class LanguagesController(TGController):

    def _before(self, *args, **kwargs):
        c.side_menu = c.doc_menu

    @expose('sauce.templates.languages')
    def index(self, *args, **kwargs):
        languages = DBSession.query(Language)
        return dict(page='language', language=None, languages=languages)

    @expose('sauce.templates.language')
    def _default(self, language_id, *args, **kwargs):
        try:
            language_id = int(language_id)
            language = DBSession.query(Language).filter_by(id=language_id).one()
        except ValueError:
            flash('Invalid Language id: %s' % language_id, 'error')
            abort(status.HTTP_400_BAD_REQUEST)
        except NoResultFound:
            flash('Language %d not found' % language_id, 'error')
            abort(status.HTTP_404_NOT_FOUND)
        except MultipleResultsFound:  # pragma: no cover
            log.error('Database inconsistency: Language %d', language_id, exc_info=True)
            flash('An error occurred while accessing Language %d' % language_id, 'error')
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

        return dict(page='language', language=language, languages=None)
