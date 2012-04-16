# -*- coding: utf-8 -*-
"""EventAdmin controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import Lesson, Team, Student
from sauce.controllers.crc import FilteredCrudRestController, TeamsCrudController, StudentsCrudController, LessonsCrudController
from sauce.lib.base import BaseController

log = logging.getLogger(__name__)


class EventAdminController(BaseController):
    
    def __init__(self, event, **kw):
        
        self.event = event
        
        menu_items = {'lesson': Lesson}
        
        self.teams = TeamsCrudController(model=Team, filters=[Team.lesson_id.in_((l.id for l in self.event.lessons))], 
                                     menu_items=menu_items, **kw)
        self.students = StudentsCrudController(model=Student, filters=[Student.id.in_((s.id for l in self.event.lessons for t in l.teams for s in t.students))], 
                                           menu_items=menu_items, **kw)
    
    @expose('sauce.templates.admin_index')
    def index(self):
        return

