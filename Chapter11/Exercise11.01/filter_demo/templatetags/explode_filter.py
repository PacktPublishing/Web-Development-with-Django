from django import template

register = template.Library()

@register.filter
def explode(value, separator):
    return value.split(separator)

