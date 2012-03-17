'''
Created on 17.03.2012

@author: moschlar
'''
from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class SubmitForm(TableForm):
    
    class fields(WidgetsList):
        #title = TextField()
        #year = TextField()
        #release_date = CalendarDatePicker()
        #genre_options = [x for x in enumerate((
        #    'Action & Adventure', 'Animation', 'Comedy',
        #    'Documentary', 'Drama', 'Sci-Fi & Fantasy'))]
        #genre = SingleSelectField(options=genre_options)
        #description = TextArea()
        source = TextArea()
        language_options = [x for x in enumerate(('C', 'Python'))]
        language = SingleSelectField(options=language_options)

submit_form = SubmitForm("submit_form")