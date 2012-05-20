# -*- coding: utf-8 -*-
"""News controller module

@author: moschlar
"""

# turbogears imports
from tg import expose, request, TGController
from tg.decorators import paginate

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import NewsItem

class NewsController(TGController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @paginate('news')
    @expose('sauce.templates.news')
    def index(self, page=1):
        '''NewsItem listing page'''
        
        news_query = NewsItem.query.filter(NewsItem.event_id == None)
        if not request.teacher:
            news_query = news_query.filter_by(public=True)
        
        #news = Page(news_query, page=page, items_per_page=20)
        
        return dict(page='news', news=news_query)
