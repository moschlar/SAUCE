<%inherit file="local:templates.master"/>

<%def name="title()">
  A ${code} Error has Occurred
</%def>

<h1>Error ${status}</h1>

<%
import re
mf = re.compile(r'(</?)script', re.IGNORECASE)
def fixmessage(message):
    return mf.sub(r'\1noscript', message)
%>

<div>${fixmessage(message) | n}</div>
