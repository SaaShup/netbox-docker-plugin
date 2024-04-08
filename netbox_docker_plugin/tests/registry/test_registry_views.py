"""Registry Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.models.host import Host
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

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")

        Registry.objects.create(host=host1, serveraddress="http://localhost:8080", name="registry0")
        Registry.objects.create(host=host1, serveraddress="http://localhost:8081", name="registry1")
        Registry.objects.create(host=host2, serveraddress="http://localhost:8082", name="registry2")

        cls.form_data = {
            "host": host1.pk,
            "name": "github",
            "serveraddress": "https://ghcr.io",
            "username": "test",
            "password": "thisisapassword",
            "email": "test@example.com",
        }
