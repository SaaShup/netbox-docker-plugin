"""Image Test Case"""

from utilities.testing import APIViewTestCases
from netbox_docker.models import Image, Host
from netbox_docker.tests.base import BaseAPITestCase


class ImageTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """Image Test Case Class"""

    model = Image
    brief_fields = ["id", "name", "provider", "size", "url", "version"]

    @classmethod
    def setUpTestData(cls) -> None:
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8080", name="host2")

        Image.objects.create(host=host1, name="image1")
        Image.objects.create(host=host1, name="image2")
        Image.objects.create(host=host2, name="image3")

        cls.create_data = [
            {
                "host": host1.pk,
                "name": "image4",
            },
            {
                "host": host1.pk,
                "name": "image5",
            },
            {
                "host": host2.pk,
                "name": "image6",
            },
        ]
