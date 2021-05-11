from django import forms
import logging

from django.utils.itercompat import is_iterable

logger = logging.getLogger(__name__)


class Select2MultipleWidget(forms.widgets.SelectMultiple):
    class Media:
        css = {
            'all': ('css/select2.min.css',)
        }
        js = ('js/modules/libs/select2.min.js', 'js/modules/functions/tags-select.js')

    def value_from_datadict(self, data, files, name):
        values = super(Select2MultipleWidget, self).value_from_datadict(data, files, name)
        return ','.join(values)

    def options(self, name, value, attrs=None):
        values = []
        for v in value:
            if not v:
                continue
            real_values = v.split(',') if hasattr(v, 'split') else v
            real_values = [real_values] if not is_iterable(real_values) else real_values
            for rv in real_values:
                values.append(rv)
        return values

    def optgroups(self, name, value, attrs=None):
        logger.error(value)
        default = [None, [], 0]
        groups = [default]

        for i, v in enumerate(self.options(name, value, attrs)):
            default[1].append(self.create_option(v, v, v, True, i))
        return groups


