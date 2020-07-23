from django import template

register = template.Library()


@register.inclusion_tag('page.html')
def pagination(num):
    return {'num': range(1, num + 1)}
