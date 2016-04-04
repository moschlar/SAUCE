# -*- coding: utf-8 -*-
'''
This module contains an OOP approach to a dynamic menu structure
based on Twitter's Bootstrap layout.

@since: 22.05.2012
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

from itertools import groupby
from tg import request, url, lurl

from webhelpers.html import literal
from webhelpers.html.tags import link_to

from sauce import model


#----------------------------------------------------------------------
# Menu class definitions
#----------------------------------------------------------------------


class Container(list):
    '''Simple container object that renders all elements in it'''

    def render(self, *args, **kw):
        return literal('').join(c.render(*args, **kw) for c in self)


class Menu(list):
    '''Base menu structure, performs rendering logic for
    different directions etc.'''

    def __init__(self, title=None, **kw):
        self.title = title
        self.kw = kw

    def render(self, *args, **kw):
        direction = kw.get('direction', 'vertical')

        if direction == 'dropdown':
            class_ = kw.get('class_dropdown', 'dropdown')
            res = literal('<li class="%s">' % (class_))
            res += literal(u'<a class="dropdown-toggle" data-toggle="dropdown" data-target="#" href="#">'
                '%s&nbsp;<b class="caret"></b></a>' % (self.title))
            res += literal(u'<ul class="dropdown-menu">')
        else:
            res = literal(u'<ul class="nav %s %s">' % (kw.get('class_menu', ''), self.kw.get('class_menu', '')))
            if self.title:
                self.insert(0, MenuHeader(self.title))
        for c in self:
            # Copy keywords to keep original kw clean
            kkw = kw.copy()
            if isinstance(c, Menu) and direction == 'horizontal':
                kkw['direction'] = 'dropdown'
            try:
                res += c.render(*args, **kkw)
            except AttributeError:
                res += literal(u'<li>' + unicode(c) + u'</li>')
        res += literal(u'</ul>')
        return res


class MenuItem(object):
    '''A menu item containing a link (to #, if None)'''

    def __init__(self, text=None, href=None, icon_name=None, class_=None, **kw):
        if text:
            self.text = text
        else:
            self.text = u''
        self.href = href
        self.icon_name = icon_name
        self.class_ = class_
        self.kw = kw

    def __unicode__(self):
        if self.icon:
            text = self.icon + u' ' + self.text
        else:
            text = self.text

        return link_to(text, self.href or u'#', **self.kw)

    @property
    def icon(self):
        if self.icon_name:
            return literal(u'<i class="icon-%s"></i>' % (self.icon_name))
        else:
            return u''

    def render(self, *args, **kw):
        return (literal(u'<li' + (u' class="%s"' % self.class_ if self.class_ else '') + u'>')
            + unicode(self) + literal(u'</li>'))


class MenuDivider(MenuItem):
    '''A menu divider'''

    def render(self, *args, **kw):
        direction = kw.get('direction', 'vertical')
        if direction == 'horizontal':
            class_ = kw.get('class_divider', 'divider-vertical')
        elif direction == 'vertical' or direction == 'dropdown':
            class_ = kw.get('class_divider', 'divider')
        else:
            class_ = ''
        return literal(u'<li class="%s"></li>' % (class_))


class MenuHeader(MenuItem):
    '''A menu header'''

    def __init__(self, content=None):
        if content:
            self.content = content
        else:
            self.content = u''

    def __unicode__(self):
        return self.content

    def render(self, *args, **kw):
        direction = kw.get('direction', 'vertical')
        if direction == 'horizontal':
            class_ = kw.get('class_header', 'navbar-text')
            return literal(u'<li><p class="%s">' % (class_) + unicode(self) + u'</p></li>')
        elif direction == 'vertical' or direction == 'dropdown':
            class_ = kw.get('class_header', 'nav-header')
            return literal(u'<li class="%s">' % (class_) + unicode(self) + u'</li>')
        else:
            return literal(unicode(self))


class Dummy(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url


#----------------------------------------------------------------------
# Menu generation functions definition
#----------------------------------------------------------------------


def separator(iter, sep):  # pylint:disable=redefined-builtin
    yield iter.next()
    for i in iter:
        yield sep() if callable(sep) else sep
        yield i


def menuitem_generic(item, **kw):
    return MenuItem(item.name, item.url, **kw)


def menu_generic(title, items, active=None):
    '''Generate generic menu structure from items

    ``items``: may be a plain list of elements or a list of tuples
    where [0] is the group heading and [1] is the list of elements
    ``active``: is the currently active element
    '''
    m = Menu(title)
    for item in items:
        if isinstance(item, tuple):
            m.append(MenuHeader(item[0]))
            for i in item[1]:
                m.append(MenuItem(i.name, i.url, class_='active' if i == active else None))
        else:
            m.append(MenuItem(item.name, item.url, class_='active' if item == active else None))
    return m


def menu_entity(obj, short=False):
    def generate_menuitems(item, last=True):
        def menu_submissions(assignment, active=None):
            # The hardest part are the submissions
            submissions = assignment.submissions_by_user(request.user, team=True)
            if submissions.count() > 0:
                s = []
                groups = groupby(submissions.all(), lambda s: s.user)
                for (user, subm) in groups:
                    if user == request.user:
                        s.insert(0, (user.display_name, list(subm)))
                    else:
                        s.append((user.display_name, list(subm)))
                submissions = s
            else:
                submissions = [(request.user.display_name, [Dummy(name='No Submissions', url='#')])]

            event = assignment.sheet.event
            if request.allowance(event):
                # Which lessons are we talking about?
                lessons = [l for l in event.lessons
                    if request.user in l.tutors
                        or request.user in event.teachers
                        or 'manage' in request.permissions]
                if lessons:
                    l = []
                    for lesson in lessons:
                        l.append(Dummy(name=u'Lesson %d: %s' % (lesson.lesson_id, lesson.name),
                            url=event.url + '/lessons/%d/submissions/sheet/%d/assignment/%d'
                                % (lesson.lesson_id, assignment.sheet.sheet_id, assignment.assignment_id)))
                    if request.user in event.teachers or 'manage' in request.permissions:
                        l.append(Dummy(name=u'All Submissions', url=assignment.url + '/submissions'))
                    submissions.append(('Lessons', l))

                submissions.append((u'Similarity', [
                    Dummy(name=u'Table', url=assignment.url + '/similarity/table'),
                    Dummy(name=u'List', url=assignment.url + '/similarity/list'),
                    Dummy(name=u'Dendrogram', url=assignment.url + '/similarity/dendrogram')
                ]))

            return menu_generic('Submissions', submissions, active)

        if item.parent:
            # Recurse first
            for i in generate_menuitems(item.parent, last=False):
                yield i

        if isinstance(item, model.Event):
            yield menuitem_generic(item)
            if last:
                yield menu_generic('Sheets', sorted(item.sheets, key=lambda s: s.sheet_id))
        elif isinstance(item, model.Sheet):
            yield menu_generic(item.name, sorted(item.parent.children, key=lambda s: s.sheet_id), item)
            if last:
                yield menu_generic('Assignments', sorted(item.assignments, key=lambda a: a.assignment_id))
        elif isinstance(item, model.Assignment):
            yield menu_generic(item.name, sorted(item.parent.children, key=lambda a: a.assignment_id), item)
            if last and request.user:
                yield menu_submissions(item)
        elif isinstance(item, model.Submission):
            yield menu_submissions(item.assignment, item)

    if short:
        # Only return first element
        return [generate_menuitems(obj).next()]
    else:
        # Insert chevrons inbetween
        return separator(generate_menuitems(obj), MenuHeader(u'<i class="icon-chevron-right icon-white"></i>'))


def menu_admin(event):
    result = []

    # Which lessons are we talking about?
    lessons = [l for l in event.lessons
        if request.user in l.tutors or request.user in event.teachers or 'manage' in request.permissions]

    if len(lessons) == 1:
        nav = Menu(u'Lesson %d: %s' % (lessons[0].lesson_id, lessons[0].name))
    elif len(lessons) > 1:
        nav = Menu(u'Lessons')
    else:
        nav = Dummy(u'', '')

    for lesson in lessons:
        if len(lessons) > 1:
            nav.append(MenuHeader(u'Lesson %d: %s' % (lesson.lesson_id, lesson.name)))
        nav.append(MenuItem(text=u'Administration',
            href=url(event.url + '/lessons/%d/' % (lesson.lesson_id)), icon_name='cog'))
        nav.append(MenuItem(text=u'Submissions', icon_name='inbox',
            href=url(event.url + '/lessons/%d/submissions' % (lesson.lesson_id))))
        qry = lesson.members_query()
        nav.append(MenuItem(text=u'eMail to Students', icon_name='envelope',
            href='mailto:%s?subject=[SAUCE]'
                % (','.join('%s' % (s.email_address)
                    for s in qry if s is not request.user)),
            onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (qry.count())))
    result.append(nav)

    if (request.user and request.user in event.teachers
            or 'manage' in request.permissions):
        nav = Menu(u'Administration')
        nav.append(MenuHeader(u'Event %s: %s' % (event._url, event.name)))
        nav.append(MenuItem(text=u'Administration',
            href=url(event.url + '/admin/'), icon_name='cog'))
        nav.append(MenuItem(text=u'Submissions', icon_name='inbox',
            href=url(event.url + '/submissions')))
        qry = event.members_query()
        nav.append(MenuItem(text=u'eMail to Students', icon_name='envelope',
            href='mailto:%s?subject=[SAUCE]'
                % (','.join('%s' % (s.email_address)
                    for s in qry if s is not request.user)),
            onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (qry.count())))
        qry = event.tutors_query()
        nav.append(MenuItem(text=u'eMail to Tutors', icon_name='envelope',
            href='mailto:%s?subject=[SAUCE]'
                % (','.join('%s' % (t.email_address)
                    for t in qry if t is not request.user)),
            onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (qry.count())))
        result.append(nav)

    # Insert divider inbetween
    return separator(iter(result), MenuDivider)


def menu(obj, short=False):
    '''Generate a full-featured menu with the hierarchy-based obj

    if short:
        only the uppermost item will be itemized, no further navigation
    '''
    c = Container()
    m = Menu()
    m.extend(menu_entity(obj, short))
    c.append(m)

    # Get the event and name it so
    event = obj
    while not isinstance(event, model.Event) and event.parent:
        event = event.parent
    if request.user in event.tutorsandteachers or 'manage' in request.permissions:
        m = Menu(class_menu='pull-right')
        m.extend(menu_admin(event))
        c.append(m)

    return c


def menu_docs(list):  # pylint:disable=redefined-builtin

    nav = Menu(u'Documentation')

    for item in list:
        if not item:
            nav.append(MenuDivider())
        elif len(item) == 1:
            nav.append(MenuHeader(*item))
        else:
            nav.append(MenuItem(*item))

    return nav


def menu_events(curr, future, prev):

    nav = Menu(u'Events')

    nav.append(MenuItem('Listing', lurl('/events'), 'th-list'))
    nav.append(MenuDivider())

    for event in curr:
        nav.append(MenuItem(event.name, event.url, not event.public and 'lock' or None))

    if future:
        nav.append(MenuDivider())
        nav.append(MenuHeader('Future'))
        for event in future:
            nav.append(MenuItem(event.name, event.url, not event.public and 'lock' or None))

    if prev:
        nav.append(MenuDivider())
        nav.append(MenuHeader('Previous'))
        for event in prev:
            nav.append(MenuItem(event.name, event.url, not event.public and 'lock' or None))

    return nav


def menu_crc(menu_items, active=None):

    nav = Menu(u'Menu')

    for (url, name) in menu_items:
        if active and (name.lower().strip('s') == active.lower().strip('s')):
            class_ = 'active'
        else:
            class_ = ''
        nav.append(MenuItem(name, url, class_=class_))

    return nav
