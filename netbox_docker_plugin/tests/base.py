"""Base Test Case Class"""

from django.urls import reverse
from utilities.testing.api import APITestCase
from utilities.testing.views import ModelViewTestCase


class BaseAPITestCase(APITestCase):
    """Base API Test Case Class"""

    def _get_detail_url(self, instance):
        viewname = f"plugins-api:{self._get_view_namespace()}:{instance._meta.model_name}-detail"
        return reverse(viewname, kwargs={"pk": instance.pk})

    def _get_list_url(self):
        viewname = f"plugins-api:{self._get_view_namespace()}:{self.model._meta.model_name}-list"
        return reverse(viewname)


class BaseModelViewTestCase(ModelViewTestCase):
    """Base API Test Case Class"""

    def _get_base_url(self):
        return (
            f"plugins:{self.model._meta.app_label}:{self.model._meta.model_name}_{{}}"
        )
