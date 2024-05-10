""" Response renderers for Django Rest Framework """

from django.utils.encoding import smart_str
from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    """ text/plain renderer """

    media_type = "text/plain"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_str(data, encoding=self.charset)
