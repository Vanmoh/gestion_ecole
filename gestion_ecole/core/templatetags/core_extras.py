# core/templatetags/core_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(d, key):
    """Accède à d[key] en template, sinon retourne 0."""
    if isinstance(d, dict):
        return d.get(key, 0)
    return 0
