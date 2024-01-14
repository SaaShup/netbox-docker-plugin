"""Volume Views Test Case"""

from utilities.testing import ViewTestCases
from netbox_docker_plugin.tests.base import BaseModelViewTestCase
from netbox_docker_plugin.models.host import Host
from netbox_docker_plugin.models.volume import Volume


class VolumeViewsTestCase(
    BaseModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    """Volume Views Test Case Class"""

    model = Volume

    @classmethod
    def setUpTestData(cls):
        host1 = Host.objects.create(endpoint="http://localhost:8080", name="host1")
        host2 = Host.objects.create(endpoint="http://localhost:8081", name="host2")

        volume1 = Volume.objects.create(name="volume1", host=host1)
        volume2 = Volume.objects.create(name="volume2", host=host2)

        cls.form_data = {
            "name": "volume3",
            "driver": "local",
            "host": host1.pk,
        }

        cls.csv_data = (
            "name,driver,host",
            f"volume4,local,{host1.pk}",
            f"volume5,,{host2.pk}",
        )

        cls.csv_update_data = (
            "id,driver",
            f"{volume1.pk},local",
            f"{volume2.pk},",
        )
