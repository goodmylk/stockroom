from django import template

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, ' ')

@register.filter(name='round_int')
def round_int(value):
    try:
        return int(round(float(value), 0))
    except ValueError:
        return value

@register.filter(name='divide_round')
def divide_round(value, arg):
    if value == None:
        return 0
    try:
        return round(float(value) / float(arg), 1)
    except (ValueError, ZeroDivisionError):
        return None
