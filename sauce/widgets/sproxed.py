'''
Created on 14.04.2012

@author: moschlar
'''

from sprox.formbase import AddRecordForm, EditableForm, Field
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from tw.forms import TextField, SingleSelectField, BooleanRadioButtonList, CalendarDateTimePicker
from tw.forms.validators import String, DateTimeConverter

from sauce.model import DBSession, Event, Lesson

class NewEventForm(AddRecordForm):
    '''Form widget for creating a new event'''
    __model__ = Event
    #__omit_fields__ = ['news', 'lessons', 'sheets', 'assignments']
    __limit_fields__ = __field_order__ = ['name', '_url', 'type', 'description', 'start_time', 'end_time', 'public', 'password', 'teacher', 'teachers']
    
    name = TextField
    _url = Field(TextField, String(min=1))
    type = SingleSelectField('type', options=[('course', 'Course'), ('contest', 'Contest')])
    start_time = Field(CalendarDateTimePicker, DateTimeConverter)
    end_time = Field(CalendarDateTimePicker, DateTimeConverter)
    password = TextField
    public = BooleanRadioButtonList

new_event_form = NewEventForm(DBSession)

class EditEventForm(EditableForm):
    ''''Form widget for editing an event'''
    __model__ = Event
    #__omit_fields__ = ['news', 'lessons', 'sheets', 'assignments', 'id']
    __limit_fields__ = __field_order__ = ['id', 'name', '_url', 'type', 'description', 'start_time', 'end_time', 'public', 'password', 'teacher', 'teachers']
    
    name = TextField
    _url = Field(TextField, String(min=1))
    type = SingleSelectField('type', options=[('course', 'Course'), ('contest', 'Contest')])
    start_time = Field(CalendarDateTimePicker, DateTimeConverter)
    end_time = Field(CalendarDateTimePicker, DateTimeConverter)
    password = TextField
    public = BooleanRadioButtonList
    
edit_event_form = EditEventForm(DBSession)

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