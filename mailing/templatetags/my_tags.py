from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'


@register.filter()
def format_str(info_str):
    return info_str[:100]
