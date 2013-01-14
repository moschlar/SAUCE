'''
Created on 14.01.2013

@author: moschlar
'''
from tgext.admin.config import AdminConfig, CrudRestControllerConfig
from sprox.fillerbase import TableFiller


class SAUCECrudRestControllerConfig(CrudRestControllerConfig):
    '''Set the table_filler_type to the default TableFiller
    
    To avoid tgext.crud from trying to perform pagination magic which
    we don't want at the moment.
    '''

    def _post_init(self):
        class MyTableFiller(TableFiller):
            __entity__ = self.model
        self.table_filler_type = MyTableFiller
        super(SAUCECrudRestControllerConfig, self)._post_init()


class SAUCEAdminConfig(AdminConfig):
    DefaultControllerConfig = SAUCECrudRestControllerConfig
