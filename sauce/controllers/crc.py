# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''

from tg import expose, tmpl_context as c
from tg.decorators import paginate, with_trailing_slash
from tgext.crud import CrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller, FillerBase, EditFormFiller

from sauce.model import DBSession, Event, Lesson, Team, User
from sprox.formbase import AddRecordForm, EditableForm

#--------------------------------------------------------------------------------

class LessonController(CrudRestController):
    model = Lesson
    
    def __init__(self, event, *args, **kw):
        super(LessonController, self).__init__(*args, **kw)
        self.event = event
    
    class table_type(TableBase):
        __model__ = Lesson
    
    class table_filler_type(TableFiller):
        __model__ = Lesson
        
        def _do_get_provider_count_and_objs(self, event, **kw):
            lessons = Lesson.query.filter_by(event_id=event.id).all()
            return len(lessons), lessons
    
    @with_trailing_slash
    @expose('tgext.crud.templates.get_all')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        c.widget = self.table
        values = self.table_filler.get_value(event=self.event, **kw)
        return dict(model=self.model.__name__, value_list=values, mount_point=self._mount_point())
    
    class new_form_type(AddRecordForm):
        __model__ = Lesson
    
    class edit_form_type(EditableForm):
        __model__ = Lesson
    
    class edit_filler_type(EditFormFiller):
        __model__ = Lesson
