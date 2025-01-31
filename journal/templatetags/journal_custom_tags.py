from django import template

register = template.Library()


@register.filter
def make_range(value):
    """
    Returns a range from 0 to the given value.
    Usage: {% for i in value|make_range %}
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return []
