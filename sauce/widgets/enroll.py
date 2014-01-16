
import tw2.core as twc
import tw2.bootstrap.forms as twbf

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as _SingleSelectField
except ImportError:  # pragma: no cover
    from tw2.forms.bootstrap import SingleSelectField as _SingleSelectField


class PasswordEnrollForm(twbf.InlineForm):
    password = twbf.PasswordField()


class LessonSelectionForm(twbf.HorizontalForm):
    event = twc.params.ChildParam()

    class lesson(_SingleSelectField):
        event = twc.params.Param()

        def prepare(self):
            self.options = [(l.id, l.name) for l in self.event.lessons]
            _SingleSelectField.prepare(self)

    def prepare(self):
        self.child.c.lesson.event = self.event
        super(LessonSelectionForm, self).prepare()


class TeamSelectionForm(twbf.HorizontalForm):
    lesson = twc.params.ChildParam()
    new = twc.params.ChildParam()

    class team(_SingleSelectField):
        lesson = twc.params.Param()
        new = twc.params.Param()

        def prepare(self):
            teams = []
            if self.new:
                teams += [('__new__', 'New Team')]
                teams += [('', '-' * 16, {'disabled': 'disabled'})]
            if self.lesson.teams:
                teams += [(t.id, t.name) for t in self.lesson.teams]
            if not teams:
                teams += [('', 'No Teams in Lesson "%s"' % (self.lesson.name))]
            self.options = [(self.lesson.name, teams)]
            _SingleSelectField.prepare(self)

    def prepare(self):
        self.child.c.team.lesson = self.lesson
        self.child.c.team.new = self.new
        super(TeamSelectionForm, self).prepare()
