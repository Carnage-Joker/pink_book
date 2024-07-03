# journal/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='lower')
def lower(value):
    return value.lower()
