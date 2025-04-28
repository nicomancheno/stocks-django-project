# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def millions(value):
    try:
        value = float(value)
        return f"{value / 1_000_000:.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def getattr(obj, attr):
    return getattr(obj, attr, None)