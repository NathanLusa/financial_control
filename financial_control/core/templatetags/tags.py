from django import template

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter('lpadzero')
def lpadzero(value, arg):
    return format(value, arg)
