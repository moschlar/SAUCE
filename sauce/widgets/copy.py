
import tw2.core as twc
import tw2.bootstrap.forms as twbf

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as _SingleSelectField
except ImportError:  # pragma: no cover
    from tw2.forms.bootstrap import SingleSelectField as _SingleSelectField


class CopyForm(twbf.InlineForm):
    required = True
    options = twc.params.ChildParam()

    selection = _SingleSelectField(label=None, css_class='span8', placeholder='Choose what to copy...')

    buttons = [
        twbf.SubmitButton('copy', value='Copy', css_class='btn btn-primary'),
    ]

    def prepare(self):
        self.child.c.selection.options = self.options
        return super(CopyForm, self).prepare()
