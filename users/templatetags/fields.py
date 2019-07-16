from django import template
from django.forms import BoundField

register = template.Library()


@register.inclusion_tag(filename='blocks/form/floating-label-field.html')
def floating_label_field(bound_field: BoundField, label: str = None, required: bool = None, **kwargs):
    """
    Таг для поля с плавающим 'label'
    """
    label = label if label is not None else bound_field.label
    required = required if required is not None else bound_field.field.required

    result = dict(
        field=bound_field,
        label=label,
        required=required,
        **kwargs
    )
    return result


@register.inclusion_tag(filename='blocks/form/checkbox.html')
def checkbox_field(bound_field: BoundField, label: str = None, required: bool = None, **kwargs):
    """
    Таг для поля типа 'checkbox'
    """
    label = label if label is not None else bound_field.label
    required = required if required is not None else bound_field.field.required

    result = dict(
        field=bound_field,
        label=label,
        required=required,
        **kwargs
    )
    return result
