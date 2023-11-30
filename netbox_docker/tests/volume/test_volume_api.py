"""Volume Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker.models.host import Host
from netbox_docker.models.volume import Volume
from netbox_docker.tests.base import BaseAPITestCase


class VolumeApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Volume Test Case Class"""

    model = Volume
    brief_fields = ["display", "driver", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Volume.objects.create(host=host1, name="volume1")
        Volume.objects.create(host=host1, name="volume2")
        Volume.objects.create(host=host2, name="volume3")

        cls.create_data = [
            {
                "host": host1.pk,
                "name": "volume4",
            },
            {
                "host": host1.pk,
                "name": "volume5",
            },
            {
                "host": host2.pk,
                "name": "volume6",
            },
        ]
