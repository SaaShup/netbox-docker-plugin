""" Response renderers for Django Rest Framework """

from django.utils.encoding import smart_str
from rest_framework import renderers


def make_content_type_renderer(content_type: str, api_format: str):
    """ Create a response renderer for the specific content type """

    class ContentTypeRenderer(renderers.BaseRenderer):
        """ content type renderer """

        media_type = content_type
        format = api_format

        def render(self, data, accepted_media_type=None, renderer_context=None):
            return smart_str(data, encoding=self.charset)

    return ContentTypeRenderer
