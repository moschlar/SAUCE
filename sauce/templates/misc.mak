
<%def name="times_dl(obj)">

<dl>
% if hasattr(obj, 'start_time'):
  <dt>Start time:</dt>
  <dd>${event.start_time.strftime('%x %X')}</dd>
% endif
% if hasattr(obj, 'end_time'):
  <dt>End time:</dt>
  <dd>${event.end_time.strftime('%x %X')}</dd>
% endif
% if hasattr(obj, 'is_active'):
  % if event.is_active:
    <dt>Remaining time:</dt>
    <dd>${h.strftimedelta(event.remaining_time)}</dd>
  % else:
    <dt>Finished.</dt>
  %endif
% endif
</dl>

</%def>