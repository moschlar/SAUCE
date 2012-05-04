# -*- coding: utf-8 -*-
"""News controller module

@author: moschlar
"""

# turbogears imports
from tg import expose, request, TGController

from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import NewsItem


class NewsController(TGController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.news')
    def index(self, page=1):
        '''NewsItem listing page'''
        
        news_query = NewsItem.query.filter(NewsItem.event_id == None).filter_by(public=not bool(request.user))
        
        news = Page(news_query, page=page, items_per_page=20)
        
        return dict(page='news', news=news)
