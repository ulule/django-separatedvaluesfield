from django.forms.widgets import Widget
from django.template import loader, Context
from django.utils.safestring import mark_safe


class SeparateValuesFieldInputWidget(Widget):

    template_name = 'widgets/separatevaluesfieldinput.html'

    def render(self, name, value, attrs=None):
        context = Context(dict(
            name=name,
            value=value
        ))
        rendered = loader.get_template(self.template_name).render(context)

        return mark_safe(rendered)