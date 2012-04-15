'''
Created on 14.04.2012

@author: moschlar
'''

from sprox.formbase import AddRecordForm, EditableForm, Field
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from tw.forms import TextField, SingleSelectField, BooleanRadioButtonList, CalendarDateTimePicker
from tw.forms.validators import String, DateTimeConverter, Int
from tw.tinymce import TinyMCE

from sauce.model import DBSession, Event, Lesson, Sheet, Assignment

#----------------------------------------------------------------------

class EventForm(object):
    '''Mixin for event form widgets'''
    __model__ = Event
    #__omit_fields__ = ['news', 'lessons', 'sheets', 'assignments']
    __limit_fields__ = __field_order__ = ['name', '_url', 'type', 'description', 'start_time', 'end_time', 'public', 'password', 'teacher', 'teachers']
    
    name = TextField
    _url = Field(TextField, String(min=1))
    type = SingleSelectField('type', options=[('course', 'Course'), ('contest', 'Contest')])
    description = TinyMCE
    start_time = Field(CalendarDateTimePicker, DateTimeConverter)
    end_time = Field(CalendarDateTimePicker, DateTimeConverter)
    password = TextField
    public = BooleanRadioButtonList

class NewEventForm(EventForm, AddRecordForm):
    '''Form widget for creating a new event'''
new_event_form = NewEventForm(DBSession)

class EditEventForm(EventForm, EditableForm):
    ''''Form widget for editing an event'''
edit_event_form = EditEventForm(DBSession)

#----------------------------------------------------------------------

class LessonTable(TableBase):
    __model__ = Lesson
    __omit_fields__ = ['__actions__']
    __limit_fields__ = __field_order__ = ['lesson_id', 'name', 'teacher', 'teams']
    __xml_fields__ = ['name']

lesson_table = LessonTable(DBSession)

class LessonTableFiller(TableFiller):
    __model__ = Lesson
    
    def name(self, obj):
        return u'<a href="%s/lessons/%d">%s</a>' % (obj.event.url, obj.id, obj.name)

lesson_filler = LessonTableFiller(DBSession)

#----------------------------------------------------------------------

class SheetForm(object):
    '''Mixin for sheet form widgets'''
    __model__ = Sheet
    #__omit_fields__ = ['news', 'lessons', 'sheets', 'assignments']
    __limit_fields__ = __field_order__ = ['name', 'sheet_id', 'description', '_start_time', '_end_time', 'public', 'teacher']
    
    name = TextField
    sheet_id = Field(TextField, Int)
    description = TinyMCE
    _start_time = Field(CalendarDateTimePicker, DateTimeConverter)
    _end_time = Field(CalendarDateTimePicker, DateTimeConverter)
    __field_widget_args__ = dict(_start_time=dict(help_text=u'Leave empty to use value from event', default=u''), 
                           _end_time=dict(help_text=u'Leave empty to use value from event', default=u''))
    
    public = BooleanRadioButtonList

class NewSheetForm(SheetForm, AddRecordForm):
    '''Form widget for creating a new sheet'''
new_sheet_form = NewSheetForm(DBSession)

class EditSheetForm(SheetForm, EditableForm):
    ''''Form widget for editing a sheet'''
edit_sheet_form = EditSheetForm(DBSession)

#----------------------------------------------------------------------

class AssignmentForm(object):
    '''Mixin for assignment form widgets'''
    __model__ = Assignment
    #__omit_fields__ = ['news', 'lessons', 'sheets', 'assignments']
    __limit_fields__ = __field_order__ = ['name', 'assignment_id', 'description', '_start_time', '_end_time', 'timeout', 'public']
    
    name = TextField
    assignment_id = Field(TextField, Int)
    description = TinyMCE
    _start_time = Field(CalendarDateTimePicker, DateTimeConverter)
    _end_time = Field(CalendarDateTimePicker, DateTimeConverter)
    __field_widget_args__ = dict(_start_time=dict(help_text=u'Leave empty to use value from event', default=u''), 
                           _end_time=dict(help_text=u'Leave empty to use value from event', default=u''))
    
    public = BooleanRadioButtonList

class NewAssignmentForm(AssignmentForm, AddRecordForm):
    '''Form widget for creating a new assignment'''
new_assignment_form = NewAssignmentForm(DBSession)

class EditAssignmentForm(AssignmentForm, EditableForm):
    ''''Form widget for editing a assignment'''
edit_assignment_form = EditAssignmentForm(DBSession)

