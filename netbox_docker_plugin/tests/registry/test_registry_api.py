"""Registry API Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker_plugin.models.registry import Registry
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
    create_data = [
        {
            "name": "github",
            "serveraddress": "https://ghcr.io",
        },
        {
            "name": "gitlab",
            "serveraddress": "http://registry.example.com",
            "username": "test",
            "password": "goodpassword",
            "email": "test@example.com",
        },
        {
            "name": "registry",
            "serveraddress": "http://localhost:1010",
        },
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        Registry.objects.create(serveraddress="http://localhost:8080", name="registry0")
        Registry.objects.create(serveraddress="http://localhost:8081", name="registry1")
        Registry.objects.create(serveraddress="http://localhost:8082", name="registry2")
