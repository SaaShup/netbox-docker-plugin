"""Registry API Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.registry import Registry
from netbox_docker_plugin.models.host import Host
from ..base import BaseAPITestCase


class RegistryApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Registry API Test Case Class"""

    model = Registry
    brief_fields = [
        "display",
        "email",
        "id",
        "name",
        "password",
        "serveraddress",
        "url",
        "username",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Registry.objects.create(
            host=host1, serveraddress="http://localhost:8080", name="registry0"
        )
        Registry.objects.create(
            host=host1, serveraddress="http://localhost:8081", name="registry1"
        )
        Registry.objects.create(
            host=host2, serveraddress="http://localhost:8082", name="registry2"
        )

        cls.create_data = [
        {
            "host": host1.pk,
            "name": "github",
            "serveraddress": "https://ghcr.io",
        },
        {
            "host": host2.pk,
            "name": "gitlab",
            "serveraddress": "http://registry.example.com",
            "username": "test",
            "password": "goodpassword",
            "email": "test@example.com",
        },
        {
            "host": host1.pk,
            "name": "registry",
            "serveraddress": "http://localhost:1010",
        },
    ]
