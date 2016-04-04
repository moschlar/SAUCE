'''

@since: 2015-01-03
@author: moschlar
'''

import inspect

from tg import abort

import status

from sprox.fillerbase import TableFiller, AddFormFiller, EditFormFiller

from sauce.controllers.crc.provider import FilterSAORMSelector


class MyTableFiller(TableFiller):

    __provider_type_selector_type__ = FilterSAORMSelector

    def __init__(self, model, actions, session, query_modifier=None, query_modifiers=None, hints=None):  # pylint:disable=too-many-arguments
        self.__model__ = self.__entity__ = model
        self.__actions__ = actions
        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers
        self.hints = hints
        super(MyTableFiller, self).__init__(session,
            query_modifier=query_modifier, query_modifiers=query_modifiers, hints=hints)


class MyEditFormFiller(EditFormFiller):

    __provider_type_selector_type__ = FilterSAORMSelector

    def __init__(self, model, session, query_modifier=None, query_modifiers=None, hints=None):  # pylint:disable=too-many-arguments
        self.__model__ = self.__entity__ = model
        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers
        self.hints = hints
        super(MyEditFormFiller, self).__init__(session,
            query_modifier=query_modifier, query_modifiers=query_modifiers, hints=hints)

    def get_value(self, values=None, **kw):
        obj = self.__provider__.get_obj(self.__entity__, params=values, fields=self.__fields__)
        if not obj:
            raise abort(status.HTTP_404_NOT_FOUND)
        values = self.__provider__.dictify(obj, self.__fields__, self.__omit_fields__)
        for key in self.__fields__:
            method = getattr(self, key, None)
            if method:
                if inspect.ismethod(method):
                    values[key] = method(obj, **kw)
        return values


class MyAddFormFiller(AddFormFiller):

    __provider_type_selector_type__ = FilterSAORMSelector

    def __init__(self, model, session, query_modifier=None, query_modifiers=None, hints=None):  # pylint:disable=too-many-arguments
        self.__model__ = self.__entity__ = model
        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers
        self.hints = hints
        super(MyAddFormFiller, self).__init__(session,
            query_modifier=query_modifier, query_modifiers=query_modifiers, hints=hints)
