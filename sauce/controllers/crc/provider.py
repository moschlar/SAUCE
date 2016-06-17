# -*- coding: utf-8 -*-
'''Custom Sprox provider that respects our filtering needs

@see: :mod:`sprox.sa`

@since: 12.01.2013
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

from warnings import warn
import inspect
import re
from tg import abort
from sprox.providerselector import _SAORMSelector, ProviderTypeSelector
from sprox.sa.provider import SAORMProvider
from sprox.sa.support import PropertyLoader, resolve_entity
from sqlalchemy import desc as _desc, func
from sqlalchemy.exc import DataError
from sqlalchemy.orm import class_mapper, Mapper
from sqlalchemy.types import Integer, Numeric
from sqlalchemy.engine import Engine

from .selectors import MyWidgetSelector, MyValidatorSelector

log = __import__('logging').getLogger(__name__)


class FilterSAORMSelector(_SAORMSelector, ProviderTypeSelector):  # pragma: no cover
    '''Selector that returns our Selector and Provider

    This class is *both* the ProviderTypeSelector as well as the ProviderSelector.
    '''

    def get_selector(self, entity=None, **hints):
        return self

    def get_provider(self, entity=None, hint=None, **hints):
        '''Based on the original _SAORMSelector'''

        if entity is None and isinstance(hint, Engine):
            engine = hint
            if engine not in self._providers:
                self._providers[engine] = FilterSAORMProvider(hint, **hints)
            return self._providers[engine]

        if hint is None and entity is not None:
            mapper = class_mapper(entity)
            hint = mapper.tables[0].bind
        engine = self._get_engine(hint, hints)
        if engine not in self._providers:
            if hint is None and len(hints) == 0:
                hint = engine
            self._providers[engine] = FilterSAORMProvider(hint, **hints)
        return self._providers[engine]


# Must inherit from object to get new-style classes
class FilterSAORMProvider(SAORMProvider, object):
    '''Provider for SQLAlchemy that respects many additional filters'''

    default_widget_selector_type = MyWidgetSelector
    default_validator_selector_type = MyValidatorSelector

    def __init__(self, session, query_modifier=None, query_modifiers=None, *args, **kwargs):
        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers or {}
        super(FilterSAORMProvider, self).__init__(session, *args, **kwargs)

    def get_dropdown_options(self, entity, field_name, view_names=None):  # pragma: no cover
        '''Getter for dropdown selection menu options

        Based on the original SAORMProvider with query_modifier(s)
        '''

        if view_names is None:
            view_names = ['_name', 'name', 'description', 'title']
        if self.session is None:  # pragma: no cover
            warn('No dropdown options will be shown for %s. '
                 'Try passing the session into the initialization '
                 'of your form base object so that this sprocket '
                 'can have values in the dropdown fields.' % entity)
            return []

        field = self.get_field(entity, field_name)

        target_field = entity
        if isinstance(field, PropertyLoader):
            target_field = field.argument
        target_field = resolve_entity(target_field)

        # some kind of relation
        if isinstance(target_field, Mapper):
            target_field = target_field.class_

        pk_fields = self.get_primary_fields(target_field)

        view_name = self.get_view_field_name(target_field, view_names)

        query = self.session.query(target_field)

        if field_name in self.query_modifiers:
            query = self.query_modifiers[field_name](query)

        rows = query

#        rows = query.all()

#        rows = self.session.query(target_field).all()

        if len(pk_fields) == 1:
            def build_pk(row):
                return getattr(row, pk_fields[0])
        else:
            def build_pk(row):
                return "/".join([str(getattr(row, pk)) for pk in pk_fields])

        return [(build_pk(row), getattr(row, view_name)) for row in rows]

    def query(self, entity, limit=None, offset=None, limit_fields=None,
            order_by=None, desc=False, field_names=[], filters={},
            substring_filters=[], **kw):  # pylint:disable=too-many-arguments

        '''Perform database query with given filters

        Based on the original SAORMProvider with query_modifier and
        some subtle enhancements (fail-safe modify_params, filter parsing)
        '''

        query = self.session.query(entity)

        if self.query_modifier:
            query = self.query_modifier(query)

        # Process filters from url
        exc = False
        try:
            filters = self._modify_params_for_dates(entity, filters)
        except ValueError as e:
            log.info('Could not parse date filters', exc_info=True)
#            flash('Could not parse date filters: %s.' % e.message, 'error')
            exc = True

        try:
            filters = self._modify_params_for_relationships(entity, filters)
        except (ValueError, AttributeError) as e:
            log.info('Could not parse relationship filters', exc_info=True)
#            flash('Could not parse relationship filters: %s. '
#                  'You can only filter by the IDs of relationships, not by their names.' % e.message, 'error')
            exc = True
        if exc:
            # Since any non-parsed filter is bad, we just have to ignore them all now
            filters = {}

        for field_name, value in filters.items():
            try:
                field = getattr(entity, field_name)
                if self.is_relation(entity, field_name) and isinstance(value, list):  # pragma: no cover
                    value = value[0]
                    query = query.filter(field.contains(value))
                else:
#                     query = query.filter(field == value)
                    typ = self.get_field(entity, field_name).type
                    if isinstance(typ, Integer):
                        value = int(value)
                        query = query.filter(field == value)
                    elif isinstance(typ, Numeric):  # pragma: no cover
                        value = float(value)
                        query = query.filter(field == value)
                    elif field_name in substring_filters and self.is_string(entity, field_name):
                        # escaped_value = re.sub('[\\\\%\\[\\]_]', '\\\\\g<0>', value.lower())
                        # query = query.filter(func.lower(field).contains(escaped_value, escape='\\'))
                        query = query.filter(func.lower(field).contains(value.lower()))
                    else:
                        query = query.filter(field == value)
            except:
                log.warn('Could not create filter on query', exc_info=True)

        # Get total count
        count = query.count()

        # Process ordering
        if order_by is not None:  # pragma: no cover
            if self.is_relation(entity, order_by):
                mapper = class_mapper(entity)
                class_ = None
                for prop in mapper.iterate_properties:
                    try:
                        class_ = prop.mapper.class_
                    except (AttributeError, KeyError):
                        pass
                query = self.session.query(entity).join(order_by)
                f = self.get_view_field_name(class_, field_names)
                field = self.get_field(class_, f)
            else:
                field = self.get_field(entity, order_by)

            if desc:
                field = _desc(field)
            query = query.order_by(field)

        # Process pager options
        if offset is not None:  # pragma: no cover
            query = query.offset(offset)
        if limit is not None:  # pragma: no cover
            query = query.limit(limit)

        return count, query

#        objs = query.all()
#
#        return count, objs

    def _get_obj(self, entity, pkdict):
        '''Get just one object with primary keys and matching modifiers'''
        pk_names = self.get_primary_fields(entity)
        pks = dict((n, pkdict[n]) for n in pk_names)
        query = self.session.query(entity)
        if self.query_modifier:
            query = self.query_modifier(query)
        query = query.reset_joinpoint().filter_by(**pks)
        try:
            obj = query.first()
        except DataError:
            obj = None
            abort(400)
#         log.debug(obj)
        return obj
