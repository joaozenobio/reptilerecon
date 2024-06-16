from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def get_file_name(value):
    return value.split('/')[-1][0:-4]
