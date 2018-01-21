from django import template

from WhoWolf import settings


register = template.Library()


@register.filter
def get_role_name(value):
    """Get name of role"""
    return settings.ROLES[value]
