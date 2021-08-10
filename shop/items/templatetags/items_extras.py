from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    if key not in d:
        return None
    return d[key]

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_attribute(obj, name):
    return getattr(obj, name)
