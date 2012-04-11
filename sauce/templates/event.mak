<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details" />

% if event:
<%def name="body_class()">navbar_left</%def>
% endif


<%def name="title()">
 ${event.name} - Event
</%def>

<h2>${event.name}</h2>

${details.event(event)}