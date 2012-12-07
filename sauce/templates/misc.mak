
<%def name="times_dl(obj)">

<dl>
% if hasattr(obj, 'start_time'):
  <dt>Start time:</dt>
  <dd>${obj.start_time.strftime('%c')}</dd>
% endif
% if hasattr(obj, 'end_time'):
  <dt>End time:</dt>
  <dd>${obj.end_time.strftime('%c')}</dd>
% endif
% if hasattr(obj, 'is_active'):
  % if obj.is_active:
    <dt>Remaining time:</dt>
    <dd>${h.strftimedelta(obj.remaining_time)}</dd>
  %endif
% endif
</dl>

</%def>