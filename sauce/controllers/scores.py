# -*- coding: utf-8 -*-
"""Scores controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
#from sauce.model import DBSession, metadata


class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.scores')
    def index(self):
        return dict(page='scores')
