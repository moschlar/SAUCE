'''
@since: 14.01.2013

@author: moschlar
'''
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
