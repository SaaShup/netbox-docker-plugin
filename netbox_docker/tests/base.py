"""Base Test Case Class"""

from django.urls import reverse
from utilities.testing.api import APITestCase

class BaseAPITestCase(APITestCase):
    """Base Test Case Class"""

    def _get_detail_url(self, instance):
        viewname = f"plugins-api:{self._get_view_namespace()}:{instance._meta.model_name}-detail"
        return reverse(viewname, kwargs={"pk": instance.pk})
