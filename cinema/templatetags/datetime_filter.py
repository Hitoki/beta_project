# -*- coding: utf-8 -*-
"""Application filter for `datetime` 24 hours.
"""

from django import template

register = template.Library()


@register.filter(name='format_datetime')
def format_datetime(value):
    hours, rem = divmod(value.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    return f'{hours}h {minutes}min'
