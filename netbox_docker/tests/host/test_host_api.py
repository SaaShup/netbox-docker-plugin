"""Host API Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker.models.host import Host
from netbox_docker.tests.base import BaseAPITestCase


class HostApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Host API Test Case Class"""

    model = Host
    brief_fields = ["display", "endpoint", "id", "name", "url"]
    create_data = [
        {
            "endpoint": "http://localhost:8083",
            "name": "host4",
        },
        {
            "endpoint": "http://localhost:8084",
            "name": "host5",
        },
        {
            "endpoint": "http://localhost:8085",
            "name": "host6",
        },
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        Host.objects.create(endpoint="http://localhost:8080", name="host1")
        Host.objects.create(endpoint="http://localhost:8081", name="host2")
        Host.objects.create(endpoint="http://localhost:8081", name="host3")
