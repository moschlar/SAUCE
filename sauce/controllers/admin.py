'''
Created on 20.03.2012

@author: moschlar
'''
from tgext.admin.config import AdminConfig, CrudRestControllerConfig
from sprox.formbase import AddRecordForm, EditableForm
from formencode import Schema
from formencode.validators import FieldsMatch, FieldStorageUploadConverter
from tw.forms import PasswordField, TextField, SingleSelectField, FileField
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sauce.model import Test, Assignment, Event





class TestCrudConfig(CrudRestControllerConfig):
    
    class new_form_type(AddRecordForm):
        __model__ = Test
        __require_fields__     = ['type']
        __omit_fields__        = ['id', 'assignment_id']
        __field_order__        = ['assignment', 'type', 'visible', 'timeout', 'argv', 'input', 'output']
        type = SingleSelectField(id='type', options=[(type,type) for type in Test.type.property.columns[0].type.enums])
        input = FileField(id='input', validator=FieldStorageUploadConverter(not_empty=False))
        output = FileField(id='output',validator=FieldStorageUploadConverter(not_empty=False))
    
    class edit_form_type(EditableForm):
        __model__ = Test
        __require_fields__     = ['type']
        __omit_fields__        = ['id', 'assignment_id']
        __field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
        type = SingleSelectField(id='type', options=[(type,type) for type in Test.type.property.columns[0].type.enums])
        input = FileField(id='input', validator=FieldStorageUploadConverter(not_empty=False), help_text='Attention, if you do not specify your input file again here, the database column will be overwritten! This bug is known and being investigated.')
        output = FileField(id='output',validator=FieldStorageUploadConverter(not_empty=False), help_text='Attention, if you do not specify your output file again here, the database column will be overwritten! This bug is known and being investigated.')
    
    class table_type(TableBase):
        __entity__ = Test
        __limit_fields__ = ['id', 'type', 'visible', 'timeout', 'assignment', 'assignment_id']
    
    class table_filler_type(TableFiller):
        __entity__ = Test
        __limit_fields__ = ['id', 'type', 'visible', 'timeout', 'assignment_id', 'assignment']

class AssignmentCrudConfig(CrudRestControllerConfig):
    
     class table_type(TableBase):
         __entity__ = Assignment
         __limit_fields__ = ['id', 'name', 'description', 'event_id', 'event', 'submissions', 'start_time', 'end_time']
     
     class table_filler_type(TableFiller):
         __entity__ = Assignment
         __limit_fields__ = ['id', 'name', 'description', 'event_id', 'event', 'submissions', 'start_time', 'end_time']

class EventCrudConfig(CrudRestControllerConfig):
    
    class new_form_type(AddRecordForm):
        __model__ = Event
        type = SingleSelectField(id='type', options=[(type,type) for type in Event.type.property.columns[0].type.enums])
    
    class edit_form_type(EditableForm):
        __model__ = Event
        type = SingleSelectField(id='type', options=[(type,type) for type in Event.type.property.columns[0].type.enums])

class MyAdminConfig(AdminConfig):
    
    default_index_template = 'mako:sauce.templates.admin_index'
    include_left_menu = False
    
    test = TestCrudConfig
    assignment = AssignmentCrudConfig
    event = EventCrudConfig
    