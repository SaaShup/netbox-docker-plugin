"""Host tag definitions"""

from re import sub
from django import template

register = template.Library()


def remove_password(value):
    """Replace password in URL by ***"""
    return sub(r"(.+):\/\/(.+):(.+)@(.+)", r"\1://\2:***@\4", value)


register.filter("remove_password", remove_password)
