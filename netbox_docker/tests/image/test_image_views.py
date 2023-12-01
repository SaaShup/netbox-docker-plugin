"""Image Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker.tests.base import BaseModelViewTestCase
from netbox_docker.models.host import Host
from netbox_docker.models.image import Image


class ImageViewsTestCase(
    BaseModelViewTestCase, ViewTestCases.PrimaryObjectViewTestCase
):
    """Image Views Test Case Class"""

    model = Image

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")
        host3 = Host.objects.create(endpoint="http://localhost:8081", name="host3")

        image1 = Image.objects.create(name="image1", host=host1)
        image2 = Image.objects.create(name="image2", host=host2)
        image3 = Image.objects.create(name="image3", host=host3)

        cls.form_data = {
            "name": "image1",
            "version": "v1.2.3",
            "provider": "github",
            "size": 512,
            "host": host1.pk,
            "ImageID": "abcdefghijklmnopqrstuvwxyz"
        }

        cls.csv_data = (
            "name,version,provider,size,host",
            f"image4,latest,github,64,{host1.pk}",
            f"image5,,,,{host2.pk}",
            f"image6,v1.2.3,,,{host3.pk}",
        )

        cls.bulk_edit_data = {"version": "v1.0.0", "provider": "github", "size": 1024}

        cls.csv_update_data = (
            "id,version,provider,size",
            f"{image1.pk},latest,,",
            f"{image2.pk},,,",
            f"{image3.pk},v1.0.0,github,256",
        )
