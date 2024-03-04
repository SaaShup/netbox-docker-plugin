"""Registry Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.models.registry import Registry
from ..base import BaseModelViewTestCase


class RegistryTestCase(
    BaseModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """Registry Views Test Case Class"""

    model = Registry
    form_data = {
        "name": "github",
        "serveraddress": "https://ghcr.io",
        "username": "test",
        "password": "thisisapassword",
        "email": "test@example.com",
    }

    @classmethod
    def setUpTestData(cls):
        Registry.objects.create(serveraddress="http://localhost:8080", name="registry0")
        Registry.objects.create(serveraddress="http://localhost:8081", name="registry1")
        Registry.objects.create(serveraddress="http://localhost:8082", name="registry2")
