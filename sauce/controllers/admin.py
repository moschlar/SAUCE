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
from sauce.model import Test


class TestAddForm(AddRecordForm):
    __model__ = Test
    __require_fields__     = ['type']
    __omit_fields__        = ['id', 'assignment_id']
    __field_order__        = ['assignment', 'type', 'visible', 'timeout', 'argv', 'input', 'output']
    
    type = SingleSelectField(id='type', options=[(type,type) for type in Test.type.property.columns[0].type.enums])
    #visible
    input = FileField(id='input', validator=FieldStorageUploadConverter(not_empty=False))
    output = FileField(id='output',validator=FieldStorageUploadConverter(not_empty=False))
    #argv
    #timeout

class TestEditForm(EditableForm):
    __model__ = Test
    __require_fields__     = ['type']
    __omit_fields__        = ['id', 'assignmend_id']
    __field_order__        = ['user_name', 'email_address', 'display_name', 'password', 'verify_password']
    #__base_validator__     = form_validator
    #email_address          = TextField
    #display_name           = TextField
    type = SingleSelectField(id='type', options=[(type,type) for type in Test.type.property.columns[0].type.enums])
    #visible
    input = FileField(id='input', validator=FieldStorageUploadConverter(not_empty=False), help_text='Attention, if you do not specify your input file again here, the database column will be overwritten! This bug is known and being investigated.')
    output = FileField(id='output',validator=FieldStorageUploadConverter(not_empty=False), help_text='Attention, if you do not specify your output file again here, the database column will be overwritten! This bug is known and being investigated.')
    #argv
    #timeout
    #verify_password        = PasswordField('verify_password')

class TestCrudConfig(CrudRestControllerConfig):
    new_form_type = TestAddForm
    edit_form_type = TestEditForm
    
    class table_type(TableBase):
        __entity__ = Test
        __limit_fields__ = ['id', 'type', 'visible', 'timeout', 'assignment', 'assignment_id']
        #__url__ = '../user.json' #this just tidies up the URL a bit

    class table_filler_type(TableFiller):
        __entity__ = Test
        __limit_fields__ = ['id', 'type', 'visible', 'timeout', 'assignment_id', 'assignment']

class MyAdminConfig(AdminConfig):
    test = TestCrudConfig
