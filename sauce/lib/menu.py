# -*- coding: utf-8 -*-
'''
This module contains an OOP approach to a dynamic menu structure
based on Twitter's Bootstrap layout.

TODO: Sorting in dropdown menus

Created on 22.05.2012
@author: moschlar
'''

from itertools import groupby
from tg import request, url

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
            res += literal(u'<a class="dropdown-toggle" data-toggle="dropdown" data-target="#" href="#">%s&nbsp;<b class="caret"></b></a>' % (self.title))
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

    def __init__(self, text=None, href=None, icon_name=None, **kw):
        if text:
            self.text = text
        else:
            self.text = u''
        self.href = href
        self.icon_name = icon_name
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
        return literal(u'<li>') + unicode(self) + literal(u'</li>')


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


#----------------------------------------------------------------------
# Menu generation functions definition
#----------------------------------------------------------------------


def separator(iter, sep):
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


def menu_entity(obj):
    def generate_menuitems(item, last=True):
        def menu_submissions(assignment, active=None):
            # The hardest part are the submissions
            submissions = assignment.submissions_by_user(request.user, team=True)
            print submissions.count(), submissions.all()
            if submissions.count() > 0:
                s, ss = [], []
                groups = groupby(submissions.all(), lambda s: s.user)
                for (user, subm) in groups:
                    if user == request.user:
                        ss.extend(list(subm))
                    else:
                        s.append((user.display_name, list(subm)))
                submissions = ss + s
            else:
                submissions = [(u'No Submissions', [])]
            return menu_generic('Submissions', submissions, active)

        menu_from_item = lambda item: menu_generic(item.name, item.parent.children, item)

        if item.parent:
            # Recurse first
            for i in generate_menuitems(item.parent, False):
                yield i

        if isinstance(item, model.Event):
            yield menuitem_generic(item)
            if last:
                yield menu_generic('Sheets', item.sheets)
        elif isinstance(item, model.Sheet):
            yield menu_from_item(item)
            if last:
                yield menu_generic('Assignments', item.assignments)
        elif isinstance(item, model.Assignment):
            yield menu_from_item(item)
            if last and request.user:
                yield menu_submissions(item)
        elif isinstance(item, model.Submission):
            yield menu_submissions(item.assignment, item)

    # Insert chevrons inbetween
    return separator(generate_menuitems(obj), MenuHeader(u'<i class="icon-chevron-right icon-white"></i>'))


def menu_admin(obj):
    # Get the event and name it so
    while not isinstance(obj, model.Event) and obj.parent:
        obj = obj.parent
    event = obj
    result = []

    # Which lessons are we talking about?
    lessons = [l for l in event.lessons
        if request.teacher == l.teacher or request.teacher == event.teacher or 'manage' in request.permissions]

    if len(lessons) == 1:
        nav = Menu(u'Lesson %d: %s' % (lessons[0].lesson_id, lessons[0].name))
    elif len(lessons) > 1:
        nav = Menu(u'Lessons')

    for lesson in lessons:
        if len(lessons) > 1:
            nav.append(MenuHeader(u'Lesson %d: %s' % (lesson.lesson_id, lesson.name)))
        nav.append(MenuItem(text=u'Administration',
            href=url(event.url + '/lessons/%d' % (lesson.lesson_id)), icon_name='cog'))
        nav.append(MenuItem(text=u'Submissions', icon_name='inbox',
            href=url(event.url + '/lessons/%d/submissions' % (lesson.lesson_id))))
        nav.append(MenuItem(text=u'eMail to Students', icon_name='envelope',
            href='mailto:%s?subject=[SAUCE]' % (','.join('%s' % (s.email_address) for s in lesson.students)),
            onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (len(lesson.students))))
    result.append(nav)

    if (request.teacher and request.teacher == event.teacher
        or 'manage' in request.permissions):
        nav = Menu(u'Administration')
        nav.append(MenuHeader(u'Event %s: %s' % (event._url, event.name)))
        nav.append(MenuItem(text=u'Administration',
            href=url(event.url + '/admin'), icon_name='cog'))
        nav.append(MenuItem(text=u'eMail to Students', icon_name='envelope',
            href='mailto:%s?subject=[SAUCE]' % (','.join('%s' % (s.email_address) for s in event.students)),
            onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (len(event.students))))
        result.append(nav)

    # Insert divider inbetween
    return separator(iter(result), MenuDivider)


def menu(obj):
    c = Container()
    m = Menu()
    m.extend(menu_entity(obj))
    c.append(m)
    if request.teacher:
        m = Menu(class_menu='pull-right')
        m.extend(menu_admin(obj))
        c.append(m)
    return c

#----------------------------------------------------------------------
# Legacy menu generation functions definition
#----------------------------------------------------------------------


def event_admin_menu(event):
    '''Build list of links for event administration navigation'''
    
    nav = Menu()
    
    if (request.teacher and request.teacher == event.teacher
        or 'manage' in request.permissions):
        sub = Menu(u'Event %s: %s' % (event._url, event.name))
        sub.append(MenuItem(text=u'Administration', href=url(event.url + '/admin'), icon_name='cog'))
        sub.append(MenuItem(text=u'eMail to Students', href='mailto:%s?subject=[SAUCE]' % (','.join('%s' % (s.email_address) for s in event.students)),
                            icon_name='envelope', onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (len(event.students))))
        nav.append(sub)
    for lesson in event.lessons:
        if request.teacher == lesson.teacher or request.teacher == event.teacher or 'manage' in request.permissions:
            sub = Menu(u'Lesson %d: %s' % (lesson.lesson_id, lesson.name))
            sub.append(MenuItem(text=u'Administration', href=url(event.url + '/lessons/%d' % (lesson.lesson_id)), icon_name='cog'))
            sub.append(MenuItem(text=u'Submissions', href=url(event.url + '/lessons/%d/submissions' % (lesson.lesson_id)), icon_name='inbox'))
            sub.append(MenuItem(text=u'eMail to Students', href='mailto:%s?subject=[SAUCE]' % (','.join('%s' % (s.email_address) for s in lesson.students)),
                                icon_name='envelope', onclick='return confirm("This will send an eMail to %d people. Are you sure?")' % (len(lesson.students))))
            nav.append(sub)
    
    return nav

def entity_menu(obj, children_header=None, children=None, icon_name='th-list', icon_name_children=True):
    '''Creates a menu structure based on a given object
    
    The supplied entity ``obj`` has to provide the following attributes:
    
    ``obj.name``:
        The human-readable identifier of the object, used as link text
    ``obj.url``:
        Link target for the object, used as link href attribute
    ``obj.parent``:
        Parent object for building the navigation list. May be ``None``
        at the top-most entity.
    
    ``children`` shall be an iterable holding entities for a child
        menu structure. The elements of ``children`` have to provide
        the mentioned attributes, too, with an exception for the
        ``parent`` attribute (which by logical conclusion should be
        obj, but that is not enforced).
    
    ``children_header`` will be the MenuHeader for the child menu.
    
    If ``icon_name_children`` is ``True``, the child menu will use the
        same icon as the parent menu. If you wish to have *no* icon at
        all, set it to ``False`` or ``None``.
    '''
    
    nav = Menu('Navigation')
    
    nav.insert(0, MenuItem(text=obj.name, href=obj.url, icon_name=icon_name))
    
    while obj.parent:
        obj = obj.parent
        nav.insert(0, MenuItem(text=obj.name, href=obj.url, icon_name=icon_name))
    
    if children:
        m = Menu(children_header)
        if icon_name_children:
            if not isinstance(icon_name_children, basestring):
                icon_name_children = icon_name
        for c in children:
            m.append(MenuItem(text=c.name, href=c.url, icon_name=icon_name_children))
        nav.append(m)
    
    return nav

def list_menu(list, icon_name=None):
    
    nav = Menu()
    
    for item in list:
        nav.append(MenuItem(*item, icon_name=icon_name))
    
    return nav
