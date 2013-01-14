# -*- coding: utf-8 -*-
"""Language controller module"""

# turbogears imports
from tg import TGController, expose, flash, abort, redirect, tmpl_context as c

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
#from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Language

log = __import__('logging').getLogger(__name__)




class LanguagesController(TGController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()

    @expose('sauce.templates.languages')
    def index(self):
        languages = DBSession.query(Language)
        return dict(page='index', language=None, languages=languages)

    @expose('sauce.templates.language')
    def _default(self, language_id, *args, **kw):
        try:
            language_id = int(language_id)
            language = DBSession.query(Language).filter_by(id=language_id).one()
        except ValueError:
            flash('Invalid Language id: %s' % language_id, 'error')
            abort(400)
        except NoResultFound:
            flash('Language %d not found' % language_id, 'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Language %d' % language_id, exc_info=True)
            flash('An error occurred while accessing Language %d' % language_id, 'error')
            abort(500)

        return dict(page='language', language=language, languages=None)
