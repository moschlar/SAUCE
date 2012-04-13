'''
Created on 13.04.2012

@author: moschlar
'''

from tw.forms import TableForm
from tw.forms.validators import Any, Empty

class ButtonTable(TableForm):
    
    params = dict(cols='Columns')
    
    template = u'''
<table>
  % for i, child in enumerate(children):
    % if (i % cols) == 0:
      <tr>
    % endif
      <td>${display_child(child)}</td>
    % if (i % cols) == cols-1:
      </tr>
    % endif
  % endfor
</table>
'''
    engine = 'mako'
    fields = []
    cols = 0
    #validator = None
