"""
Custom filter for getting the value of a variable-key in a dictionary.
"""

from django import template

register = template.Library()


@register.filter(name='get_key')
def get_key(dictionary, key):
    if key:
        return dictionary.get(key)
