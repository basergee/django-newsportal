from django import template

register = template.Library()


@register.filter()
def censor(text_to_filter):
    filtered_text = 'None shall pass'
    return filtered_text
