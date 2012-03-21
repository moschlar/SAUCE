# -*- coding: utf-8 -*-
"""News controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

from sqlalchemy.sql import desc

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, NewsItem


class NewsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.news')
    def index(self, page=1):
        
        news_query = DBSession.query(NewsItem).order_by(desc(NewsItem.date))
        
        news = Page(news_query, page=page, items_per_page=20)
        
        return dict(page='news', news=news)
