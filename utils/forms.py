from typing import Union

from django import forms


class StyledForm(forms.Form):

    _js_class_prefix = 'js-field_'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.get_field_items():

            css_class = field.widget.attrs.get('class', '')
            css_class += f' {self._js_class_prefix}{field_name}'
            field.widget.attrs.update({
                'class': css_class
            })

    def get_field_items(self):
        return self.fields.copy().items()
