# dressup/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter(name='replace')
def replace(value, args):
    """
    Replaces all occurrences of the first argument with the second argument.
    Usage: {{ value|replace:"_, " }}
    """
    try:
        old, new = args.split(',')
        return value.replace(old.strip(), new.strip())
    except ValueError:
        # If the format is incorrect, return the original value
        return value


@register.filter
def concat(*args):
    return ''.join(args)


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None
    

