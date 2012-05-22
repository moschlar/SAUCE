# -*- coding: utf-8 -*-
'''
Created on 22.05.2012

@author: moschlar
'''

from tg import request, url

from webhelpers.html import literal
from webhelpers.html.tags import link_to

class Menu(list):
    
    def __init__(self, title=None):
        self.title = title
    
    def render(self, *args, **kw):
        direction = kw.get('direction', 'vertical')
        
        if direction == 'dropdown':
            class_ = kw.get('class_dropdown', 'dropdown')
            res = literal('<li class="%s">' % (class_))
            res += literal(u'<a class="dropdown-toggle" data-toggle="dropdown" data-target="#" href="#">%s <b class="caret"></b></a>' % (self.title))
            res += literal(u'<ul class="dropdown-menu">')
        else:
            res = literal(u'<ul class="nav %s">' % kw.get('class_menu', ''))
            if self.title:
                self.insert(0, MenuHeader(self.title))
        for c in self:
            if isinstance(c, Menu) and direction == 'horizontal':
                kw['direction'] = 'dropdown'
            try:
                res += c.render(*args, **kw)
            except AttributeError:
                res += literal(u'<li>' + unicode(c) + u'</li>')
        res += literal(u'</ul>')
        return res

class MenuItem(object):
    
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
        
        if self.href:
            return link_to(text, self.href, **self.kw)
        else:
            return text
    
    @property
    def icon(self):
        if self.icon_name:
            return literal(u'<i class="icon-%s"></i>' % (self.icon_name))
        else:
            return u''
    
    def render(self, *args, **kw):
        return literal(u'<li>') + unicode(self) + literal(u'</li>')

class MenuDivider(MenuItem):
    def render(self, *args, **kw):
        direction = kw.get('direction', 'vertical')
        if direction == 'horizontal':
            class_ = kw.get('class_divider', 'divider-vertical')
        elif direction == 'vertical':
            class_ = kw.get('class_divider', 'divider')
        else:
            class_ = ''
        return literal(u'<li class="%s"></li>' % (class_))

class MenuHeader(MenuItem):
    
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
        elif direction == 'vertical':
            class_ = kw.get('class_header', 'nav-header')
            return literal(u'<li class="%s">' % (class_) + unicode(self) + u'</li>')
        else:
            return literal(unicode(self))

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
