"""Image Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.image import Image


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
            "host": host1.pk
        }

        cls.csv_data = (
            "name,version,provider,host",
            f"image4,latest,github,{host1.pk}",
            f"image5,,,{host2.pk}",
            f"image6,v1.2.3,,{host3.pk}",
        )

        cls.bulk_edit_data = {"version": "v1.0.0", "provider": "github"}

        cls.csv_update_data = (
            "id,version,provider",
            f"{image1.pk},latest,",
            f"{image2.pk},,",
            f"{image3.pk},v1.0.0,github",
        )
