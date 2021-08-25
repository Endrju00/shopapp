from django import template

register = template.Library()

@register.filter
def multiple(arg1, arg2):
    return arg1 * arg2
